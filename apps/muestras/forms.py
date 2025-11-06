from django import forms
from .models import Muestra
from usuarios.models import Usuario

class MuestraCreateForm(forms.ModelForm):
    """
    Formulario para registrar la toma/recepción de una muestra.
    """
    class Meta:
        model = Muestra
        # El 'estado' se pone por defecto en 'Recepcionada'
        fields = ['tipo_muestra', 'responsable_toma', 'codigo_barras', 'fecha_toma', 'observaciones']
        widgets = {
            'tipo_muestra': forms.Select(attrs={'class': 'form-select'}),
            'responsable_toma': forms.Select(attrs={'class': 'form-select'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej: A-10245'}),
            'fecha_toma': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # 'tipos_requeridos' es una lista de IDs que pasaremos desde la vista
        tipos_requeridos = kwargs.pop('tipos_requeridos', None)
        # 'usuario_actual' lo pasaremos desde la vista
        usuario_actual = kwargs.pop('usuario_actual', None)
        
        super().__init__(*args, **kwargs)
        
        if tipos_requeridos:
            # Filtramos el dropdown para mostrar SÓLO los tipos de muestra
            # que esta orden necesita y que AÚN NO se han registrado.
            self.fields['tipo_muestra'].queryset = tipos_requeridos
        
        if usuario_actual:
            # Asignamos el responsable por defecto
            self.fields['responsable_toma'].queryset = Usuario.objects.filter(pk=usuario_actual.pk)
            self.fields['responsable_toma'].initial = usuario_actual
            self.fields['responsable_toma'].widget.attrs['readonly'] = True


class MuestraUpdateForm(forms.ModelForm):
    """
    Formulario simple para que el personal de laboratorio
    actualice el estado de la muestra (Trazabilidad).
    """
    class Meta:
        model = Muestra
        fields = ['estado', 'codigo_barras', 'observaciones']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }