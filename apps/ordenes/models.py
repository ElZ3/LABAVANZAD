from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal, ROUND_HALF_UP
from django.db.models import Sum

# Importamos los modelos de las otras apps
from pacientes.models import Paciente
from examenes.models import Examen
from paquetes.models import Paquete
# IMPORTANTE: Importamos los modelos de Convenio para leer los descuentos
from convenios.models import Convenio, ConvenioExamen, ConvenioPaquete 

# Constante de IVA (Ej: 13%)
IVA_PORCENTAJE = Decimal('0.13')

class Orden(models.Model):
    orden_id = models.AutoField(primary_key=True)
    
    # --- Relaciones ---
    paciente = models.ForeignKey(Paciente, on_delete=models.PROTECT, verbose_name="Paciente")
    convenio = models.ForeignKey(
        Convenio,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='ordenes',
        verbose_name="Convenio"
    )
    
    # Relaciones M2M
    examenes = models.ManyToManyField(Examen, through='OrdenExamen', related_name='ordenes', blank=True)
    paquetes = models.ManyToManyField(Paquete, through='OrdenPaquete', related_name='ordenes', blank=True)
    
    # --- Estado y Prioridad ---
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),
        ('En Proceso', 'En Proceso'),
        ('Completada', 'Completada'),
        ('Cancelada', 'Cancelada'),
    ]
    PRIORIDAD_CHOICES = [('Rutina', 'Rutina'), ('Preferente', 'Preferente'), ('Urgente', 'Urgente')]
    ENTREGA_CHOICES = [('Correo', 'Correo'), ('WhatsApp', 'WhatsApp'), ('Impreso', 'Impreso'), ('Teléfono', 'Teléfono')]
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente', blank=False)
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='Rutina', blank=False)
    metodo_entrega = models.CharField(max_length=20, choices=ENTREGA_CHOICES, default='Impreso', blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # --- Facturación ---
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_con_iva = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    monto_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    ESTADO_PAGO_CHOICES = [
        ('Pendiente', 'Pendiente de Pago'),
        ('Parcial', 'Pago Parcial'),
        ('Pagada', 'Pagada'),
        ('Anulada', 'Anulada'),
    ]
    estado_pago = models.CharField(max_length=20, choices=ESTADO_PAGO_CHOICES, default='Pendiente')

    def __str__(self):
        return f"Orden #{self.orden_id} - {self.paciente.nombre}"

    # ==============================================================================
    # === LÓGICA DE NEGOCIO: APLICACIÓN DE DESCUENTOS ===
    # ==============================================================================
    def calcular_totales(self):
        """
        Recorre todos los ítems de la orden, verifica si el convenio tiene
        descuentos aplicables (Específico > General) y actualiza los precios.
        """
        total_precio_base = Decimal('0.00') # Precio sin descuento (para calcular cuánto se ahorró)
        nuevo_subtotal = Decimal('0.00')    # Precio con descuento

        # --- 1. PROCESAR EXÁMENES ---
        # Usamos select_related para optimizar la consulta a la DB
        for item in self.ordenexamen_set.select_related('examen').all():
            precio_base = item.examen.precio
            descuento_pct = Decimal('0.00')

            # Solo aplicamos lógica si hay un convenio seleccionado
            if self.convenio:
                # A. Nivel 1: ¿Existe un descuento ESPECÍFICO para este examen?
                try:
                    desc_obj = ConvenioExamen.objects.get(convenio=self.convenio, examen=item.examen)
                    descuento_pct = desc_obj.porcentaje_descuento
                except ConvenioExamen.DoesNotExist:
                    # B. Nivel 2: Si no, usar descuento GENERAL de exámenes
                    descuento_pct = self.convenio.descuento_general_examenes

            # Calcular el precio final para este ítem
            # Fórmula: Precio * (1 - (Descuento / 100))
            factor = (Decimal('100') - descuento_pct) / Decimal('100')
            precio_final = (precio_base * factor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            # Guardamos el precio calculado en la línea de la orden (Snapshot)
            if item.precio_en_orden != precio_final:
                item.precio_en_orden = precio_final
                item.save()

            total_precio_base += precio_base
            nuevo_subtotal += precio_final

        # --- 2. PROCESAR PAQUETES ---
        for item in self.ordenpaquete_set.select_related('paquete').all():
            precio_base = item.paquete.precio
            descuento_pct = Decimal('0.00')

            if self.convenio:
                # A. Nivel 1: Descuento ESPECÍFICO para este paquete
                try:
                    desc_obj = ConvenioPaquete.objects.get(convenio=self.convenio, paquete=item.paquete)
                    descuento_pct = desc_obj.porcentaje_descuento
                except ConvenioPaquete.DoesNotExist:
                    # B. Nivel 2: Descuento GENERAL de paquetes
                    descuento_pct = self.convenio.descuento_general_paquetes

            factor = (Decimal('100') - descuento_pct) / Decimal('100')
            precio_final = (precio_base * factor).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
            
            if item.precio_en_orden != precio_final:
                item.precio_en_orden = precio_final
                item.save()

            total_precio_base += precio_base
            nuevo_subtotal += precio_final

        # --- 3. GUARDAR TOTALES GLOBALES ---
        self.subtotal = nuevo_subtotal
        # El descuento aplicado es la diferencia entre el precio de lista y lo que se cobra
        self.descuento_aplicado = total_precio_base - nuevo_subtotal
        
        # Cálculo de IVA (13%) sobre el subtotal con descuento
        self.iva = (self.subtotal * IVA_PORCENTAJE).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        self.total_con_iva = (self.subtotal + self.iva).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        self.save()
        
        # Actualizar si está pagada o pendiente
        self.actualizar_estado_pago()

    def actualizar_estado_pago(self):
        if self.estado == 'Cancelada':
            self.estado_pago = 'Anulada'
            self.monto_pagado = Decimal('0.00')
            self.save()
            return

        total_pagado = self.pagos.all().aggregate(Sum('monto'))['monto__sum'] or Decimal('0.00')
        self.monto_pagado = total_pagado.quantize(Decimal('0.01'))

        # Usamos una pequeña tolerancia por seguridad
        if self.monto_pagado >= self.total_con_iva:
            self.estado_pago = 'Pagada'
        elif self.monto_pagado > 0:
            self.estado_pago = 'Parcial'
        else:
            self.estado_pago = 'Pendiente'
            
        self.save()
        
        # Sincronizar con la factura si existe
        if hasattr(self, 'factura'):
            self.factura.estado = self.estado_pago
            self.factura.save()

    class Meta:
        db_table = 'Ordenes'
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"
        ordering = ['-fecha_creacion']

# --- Tablas Intermedias (Sin cambios) ---

class OrdenExamen(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.PROTECT)
    precio_en_orden = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'Ordenes_Examenes'
        unique_together = ('orden', 'examen')

class OrdenPaquete(models.Model):
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    paquete = models.ForeignKey(Paquete, on_delete=models.PROTECT)
    precio_en_orden = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        db_table = 'Ordenes_Paquetes'
        unique_together = ('orden', 'paquete')