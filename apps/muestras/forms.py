from django import forms
from .models import Muestra
from usuarios.models import Usuario

class MuestraCreateForm(forms.ModelForm):
    class Meta:
        model = Muestra
        fields = ['tipo_muestra', 'responsable_toma', 'codigo_barras', 'fecha_toma', 'observaciones']
        widgets = {
            'tipo_muestra': forms.Select(attrs={'class': 'form-select'}),
            'responsable_toma': forms.Select(attrs={'class': 'form-select'}),
            # CAMBIO: Readonly para el código automático
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control bg-light', 'readonly': 'readonly'}),
            'fecha_toma': forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'}),
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        # 1. Extraer argumentos personalizados
        tipos_requeridos_qs = kwargs.pop('tipos_requeridos_qs', None)
        usuario_actual = kwargs.pop('usuario_actual', None)

        # 2. Inicializar
        super().__init__(*args, **kwargs)

        # 3. Aplicar filtro de muestras (SOLO LAS NECESARIAS)
        if tipos_requeridos_qs is not None:
            self.fields['tipo_muestra'].queryset = tipos_requeridos_qs
            self.fields['tipo_muestra'].empty_label = "Seleccione el tipo de muestra a registrar"
        
        # 4. Fijar usuario actual
        if usuario_actual:
            self.fields['responsable_toma'].queryset = Usuario.objects.filter(pk=usuario_actual.pk)
            self.fields['responsable_toma'].initial = usuario_actual
            # Opcional: deshabilitar visualmente
            # self.fields['responsable_toma'].widget.attrs['style'] = 'pointer-events: none; background-color: #e9ecef;'

# (MuestraUpdateForm se mantiene igual)
class MuestraUpdateForm(forms.ModelForm):
    class Meta:
        model = Muestra
        fields = ['estado', 'codigo_barras', 'observaciones']
        widgets = {
            'estado': forms.Select(attrs={'class': 'form-select'}),
            'codigo_barras': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}), # También readonly al editar
            'observaciones': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }