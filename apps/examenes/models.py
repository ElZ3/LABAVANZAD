from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from categorias.models import CategoriaExamen
from tipos_muestras.models import TipoMuestra

# Opciones de Estado reutilizables
ESTADO_CHOICES = [('Activo', 'Activo'), ('Inactivo', 'Inactivo')]

class Examen(models.Model):
    """
    Modelo principal para un examen de laboratorio.
    """
    examen_id = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100, unique=True, blank=False)
    codigo = models.CharField(max_length=20, unique=True, blank=False,
                              help_text="Código corto o mnemotécnico (Ej: GLU, HMG)")
    precio = models.DecimalField(max_digits=8, decimal_places=2, blank=False,
                                 validators=[MinValueValidator(0.01)])

    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)

    # --- RELACIONES ---
    categoria = models.ForeignKey(
        CategoriaExamen,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name="Categoría"
    )
    tipo_muestra = models.ForeignKey(
        TipoMuestra,
        on_delete=models.PROTECT,
        blank=False, null=False,
        verbose_name="Tipo de Muestra Requerido"
    )

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

    # --- REGLAS DE NEGOCIO (Arquitectura) ---
    def puede_eliminarse(self):
        """ Regla de negocio: No borrar si tiene resultados de pacientes. """
        # (Lógica futura)
        # Ejemplo: if self.resultados.exists(): return (False, "...")
        return (True, None)

    def delete(self, *args, **kwargs):
        """ Sobrescribe el borrado para aplicar la regla de negocio. """
        se_puede, razon = self.puede_eliminarse()
        if not se_puede:
            raise ValidationError(razon)
        # Hijos (Metodos, Valores) se borran en CASCADA.
        super().delete(*args, **kwargs)

    class Meta:
        db_table = 'Examenes'
        verbose_name = "Examen"
        verbose_name_plural = "Exámenes"
        ordering = ['categoria', 'nombre']


class MetodoExamen(models.Model):
    """
    Modelo "hijo" para los métodos. Ahora incluye un estado.
    """
    metodo_examen_id = models.AutoField(primary_key=True)
    examen = models.ForeignKey(
        Examen, 
        on_delete=models.CASCADE, 
        related_name='metodos'
    )
    metodo = models.CharField(max_length=100, blank=False,
                             help_text="Ej: Espectrofotometría, Inmunoensayo")
    
    # REQUISITO: Añadir estado para inactivar en lugar de borrar
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)

    def __str__(self):
        return f"{self.metodo} ({self.estado})"
    
    class Meta:
        db_table = 'Examenes_Metodos'
        verbose_name = "Método del Examen"
        verbose_name_plural = "Métodos del Examen"


class ValorReferencia(models.Model):
    # ... (ID y FK a Examen igual que antes) ...
    valor_referencia_id = models.AutoField(primary_key=True)
    examen = models.ForeignKey(Examen, on_delete=models.CASCADE, related_name='valores_referencia')

    # --- NUEVOS CAMPOS DE CLASIFICACIÓN ---
    SEXO_APLICABLE = [
        ('Indistinto', 'Ambos Sexos'),
        ('M', 'Masculino'),
        ('F', 'Femenino'),
    ]
    sexo = models.CharField(
        max_length=10, 
        choices=SEXO_APLICABLE, 
        default='Indistinto',
        verbose_name="Sexo"
    )
    
    # Rango de edad en AÑOS (Ej: 0 a 120)
    edad_minima = models.PositiveIntegerField(default=0, verbose_name="Edad Mín (Años)")
    edad_maxima = models.PositiveIntegerField(default=120, verbose_name="Edad Máx (Años)")
    
    # --- CAMPOS DE VALOR (Igual que antes) ---
    rango_referencia = models.CharField(max_length=100, blank=False, verbose_name="Rango o Valor")
    unidad_medida = models.CharField(max_length=50, blank=True, verbose_name="Unidad")
    
    TIPO_RESULTADO_CHOICES = [
        ('Cuantitativo', 'Cuantitativo (Número)'),
        ('Cualitativo', 'Cualitativo (Texto)'),
    ]
    tipo_resultado = models.CharField(
        max_length=20, choices=TIPO_RESULTADO_CHOICES, default='Cuantitativo'
    )
    
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo')

    # Generamos el texto automáticamente para que se lea bonito
    def __str__(self):
        sexo_txt = "" if self.sexo == 'Indistinto' else f"{self.get_sexo_display()} "
        edad_txt = ""
        if self.edad_minima > 0 or self.edad_maxima < 120:
            edad_txt = f"({self.edad_minima}-{self.edad_maxima} años): "
        
        return f"{sexo_txt}{edad_txt}{self.rango_referencia} {self.unidad_medida}"

    class Meta:
        db_table = 'Examenes_Valores_Referencia'
        verbose_name = "Valor de Referencia"
        verbose_name_plural = "Valores de Referencia"