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
    """
    Modelo "hijo" para los valores/parámetros. Ahora incluye un estado.
    """
    valor_referencia_id = models.AutoField(primary_key=True)
    examen = models.ForeignKey(
        Examen, 
        on_delete=models.CASCADE, 
        related_name='valores_referencia'
    )
    
    poblacion = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Ej: Hombres, Mujeres, Niños (Dejar en blanco si es general)"
    )
    rango_referencia = models.CharField(
        max_length=100, 
        blank=False,
        verbose_name="Rango o Valor",
        help_text="Ej: 120 - 200, Negativo, < 10"
    )
    unidad_medida = models.CharField(
        max_length=50,
        blank=True, 
        verbose_name="Unidad de Medida",
        help_text="Ej: mg/dL (Dejar en blanco si no aplica)"
    )
    TIPO_RESULTADO_CHOICES = [
        ('Cuantitativo', 'Cuantitativo (Número)'),
        ('Cualitativo', 'Cualitativo (Texto)'),
    ]
    tipo_resultado = models.CharField(
        max_length=20,
        choices=TIPO_RESULTADO_CHOICES,
        blank=False,
        default='Cuantitativo',
        verbose_name="Tipo de Resultado"
    )
    
    # REQUISITO: Añadir estado para inactivar en lugar de borrar
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='Activo', blank=False)

    def __str__(self):
        pob = f"{self.poblacion}: " if self.poblacion else ""
        uni = f" {self.unidad_medida}" if self.unidad_medida else ""
        return f"{pob}{self.rango_referencia}{uni} ({self.estado})"

    class Meta:
        db_table = 'Examenes_Valores_Referencia'
        verbose_name = "Valor de Referencia"
        verbose_name_plural = "Valores de Referencia"