from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from decimal import Decimal

# Importamos los modelos de las otras apps
from pacientes.models import Paciente
from examenes.models import Examen
from convenios.models import Convenio
from paquetes.models import Paquete

class Orden(models.Model):
    """
    Modelo principal de la Orden. Almacena la información del paciente,
    convenio, estado, y las relaciones M2M a exámenes y paquetes.
    """
    orden_id = models.AutoField(primary_key=True)
    
    # --- Relaciones Principales ---
    paciente = models.ForeignKey(
        Paciente, 
        on_delete=models.PROTECT, # No borrar paciente si tiene órdenes
        null=False, blank=False,
        verbose_name="Paciente"
    )
    convenio = models.ForeignKey(
        Convenio,
        on_delete=models.SET_NULL, # Si se borra el convenio, la orden queda
        null=True, blank=True, # El convenio es opcional
        verbose_name="Convenio"
    )
    
    # --- Relaciones M2M (La Clave) ---
    examenes = models.ManyToManyField(
        Examen,
        through='OrdenExamen', # Usamos 'through' para guardar el precio
        related_name='ordenes',
        blank=True
    )
    paquetes = models.ManyToManyField(
        Paquete,
        through='OrdenPaquete', # Usamos 'through' para guardar el precio
        related_name='ordenes',
        blank=True
    )
    
    # --- Estado y Prioridad (de tu tabla) ---
    ESTADO_CHOICES = [
        ('Pendiente', 'Pendiente'),     # Recién creada, pendiente de pago/toma
        ('En Proceso', 'En Proceso'), # Muestra tomada, en análisis
        ('Completada', 'Completada'),   # Resultados listos
        ('Cancelada', 'Cancelada'),     # Orden anulada
    ]
    PRIORIDAD_CHOICES = [
        ('Rutina', 'Rutina'),
        ('Preferente', 'Preferente'),
        ('Urgente', 'Urgente'),
    ]
    ENTREGA_CHOICES = [
        ('Correo', 'Correo'),
        ('WhatsApp', 'WhatsApp'),
        ('Impreso', 'Impreso'),
        ('Teléfono', 'Teléfono'),
    ]
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Pendiente', blank=False)
    prioridad = models.CharField(max_length=20, choices=PRIORIDAD_CHOICES, default='Rutina', blank=False)
    metodo_entrega = models.CharField(max_length=20, choices=ENTREGA_CHOICES, default='Impreso', blank=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    
    # --- Campos de Costos (Calculados) ---
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    descuento_aplicado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total_pagado = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Orden #{self.orden_id} - {self.paciente.nombre} {self.paciente.apellido}"

    def calcular_totales(self):
        """
        LÓGICA DE NEGOCIO: Calcula y guarda el subtotal, descuento y total.
        Llamado cada vez que se añade o quita un ítem.
        """
        subtotal_examenes = sum(item.precio_en_orden for item in self.ordenexamen_set.all())
        subtotal_paquetes = sum(item.precio_en_orden for item in self.ordenpaquete_set.all())
        
        self.subtotal = (subtotal_examenes + subtotal_paquetes).quantize(Decimal('0.01'))
        
        # Lógica de Descuento (basada en el modelo Convenio que NO tiene descuento)
        # Si en el futuro añades 'descuento_porcentaje' a Convenio, esta lógica funcionará.
        descuento_total = Decimal('0.00')
        # if self.convenio and hasattr(self.convenio, 'descuento_porcentaje'):
        #     porcentaje = Decimal(str(self.convenio.descuento_porcentaje / 100.0))
        #     descuento_total = self.subtotal * porcentaje
        
        self.descuento_aplicado = descuento_total.quantize(Decimal('0.01'))
        self.total_pagado = (self.subtotal - self.descuento_aplicado).quantize(Decimal('0.01'))
        
        self.save()

    class Meta:
        db_table = 'Ordenes'
        verbose_name = "Orden"
        verbose_name_plural = "Órdenes"
        ordering = ['-fecha_creacion']

class OrdenExamen(models.Model):
    """
    Tabla intermedia: Orden <-> Examen
    Guarda el precio del examen EN ESE MOMENTO.
    """
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    examen = models.ForeignKey(Examen, on_delete=models.PROTECT) # Proteger examen
    precio_en_orden = models.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        db_table = 'Ordenes_Examenes'
        unique_together = ('orden', 'examen') # No añadir el mismo examen dos veces

class OrdenPaquete(models.Model):
    """
    Tabla intermedia: Orden <-> Paquete
    Guarda el precio del paquete EN ESE MOMENTO.
    """
    orden = models.ForeignKey(Orden, on_delete=models.CASCADE)
    paquete = models.ForeignKey(Paquete, on_delete=models.PROTECT) # Proteger paquete
    precio_en_orden = models.DecimalField(max_digits=8, decimal_places=2)
    
    class Meta:
        db_table = 'Ordenes_Paquetes'
        unique_together = ('orden', 'paquete') # No añadir el mismo paquete dos veces