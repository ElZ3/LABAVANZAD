from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import ValidationError
from django.db.models.deletion import ProtectedError
from .models import Paquete, PaqueteExamen
from .forms import PaqueteForm, PaqueteExamenForm
from django.db import transaction

# --- Mixin de Seguridad (Mismo que exámenes) ---
class AdminTecnicoJefeRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    def test_func(self):
        if not self.request.user.is_authenticated or not self.request.user.rol:
            return False
        roles_permitidos = ['Administrador', 'Tecnico', 'Jefe de Laboratorio']
        return self.request.user.rol.nombre in roles_permitidos
    
    def handle_no_permission(self):
        messages.error(self.request, "No tienes permiso para acceder a esta página.")
        return redirect('dashboard' if self.request.user.is_authenticated else 'login')

# ===============================================
# === CRUD para Paquete
# ===============================================

class PaqueteListView(AdminTecnicoJefeRequiredMixin, ListView):
    model = Paquete
    template_name = 'paquetes/paquete_lista.html'
    context_object_name = 'paquetes'
    queryset = Paquete.objects.prefetch_related('examenes')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Agregar estadísticas para el template
        paquetes = context['paquetes']
        context['total_paquetes'] = paquetes.count()
        context['paquetes_activos'] = paquetes.filter(estado='Activo').count()
        context['paquetes_inactivos'] = paquetes.filter(estado='Inactivo').count()
        return context

class PaqueteCreateView(AdminTecnicoJefeRequiredMixin, CreateView):
    model = Paquete
    form_class = PaqueteForm
    template_name = 'paquetes/paquete_registrar.html'
    success_url = reverse_lazy('paquetes:paquete_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = "Registrar Nuevo Paquete"
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Guardar el paquete primero
                self.object = form.save()
                
                # Guardar la relación many-to-many con exámenes
                examenes = form.cleaned_data['examenes']
                
                # Crear las relaciones usando bulk_create para mejor performance
                paquete_examenes = []
                for examen in examenes:
                    # Verificar si ya existe la relación (por si acaso)
                    if not PaqueteExamen.objects.filter(paquete=self.object, examen=examen).exists():
                        paquete_examenes.append(
                            PaqueteExamen(
                                paquete=self.object,
                                examen=examen,
                                estado='Activo',
                                orden=0
                            )
                        )
                
                if paquete_examenes:
                    PaqueteExamen.objects.bulk_create(paquete_examenes)
                
                messages.success(self.request, "Paquete creado exitosamente.")
                return redirect(self.success_url)
                
        except Exception as e:
            messages.error(self.request, f"Error al crear el paquete: {str(e)}")
            return self.form_invalid(form)

class PaqueteUpdateView(AdminTecnicoJefeRequiredMixin, UpdateView):
    model = Paquete
    form_class = PaqueteForm
    template_name = 'paquetes/paquete_editar.html'
    success_url = reverse_lazy('paquetes:paquete_list')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Paquete: {self.object.nombre}"
        
        # Obtener los exámenes del paquete con su información de estado y orden
        examenes_detalle = PaqueteExamen.objects.filter(
            paquete=self.object
        ).select_related('examen').order_by('orden')
        context['examenes_detalle'] = examenes_detalle
        
        return context

    def form_valid(self, form):
        try:
            with transaction.atomic():
                # Obtener exámenes seleccionados en el formulario
                examenes_seleccionados = set(form.cleaned_data['examenes'])
                
                # Obtener exámenes actuales del paquete
                examenes_actuales = set(self.object.examenes.all())
                
                # Exámenes a añadir
                examenes_a_anadir = examenes_seleccionados - examenes_actuales
                for examen in examenes_a_anadir:
                    # Verificar si ya existe (podría estar inactivo)
                    paquete_examen, created = PaqueteExamen.objects.get_or_create(
                        paquete=self.object,
                        examen=examen,
                        defaults={
                            'estado': 'Activo',
                            'orden': 0
                        }
                    )
                    if not created:
                        # Si ya existe pero está inactivo, reactivarlo
                        paquete_examen.estado = 'Activo'
                        paquete_examen.save()
                
                # Exámenes a remover (cambiar estado a Inactivo en lugar de eliminar)
                examenes_a_remover = examenes_actuales - examenes_seleccionados
                PaqueteExamen.objects.filter(
                    paquete=self.object,
                    examen__in=examenes_a_remover
                ).update(estado='Inactivo')
                
                messages.success(self.request, "Paquete actualizado exitosamente.")
                return super().form_valid(form)
                
        except Exception as e:
            messages.error(self.request, f"Error al actualizar el paquete: {str(e)}")
            return self.form_invalid(form)
        
class PaqueteDeleteView(AdminTecnicoJefeRequiredMixin, DeleteView):
    model = Paquete
    template_name = 'paquetes/paquete_confirm_delete.html'
    success_url = reverse_lazy('paquetes:paquete_list')

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
            messages.success(request, f"Paquete '{self.object.nombre}' eliminado exitosamente.")
        except (ValidationError, ProtectedError) as e:
            error_message = e.message if isinstance(e, ValidationError) else str(e)
            messages.error(request, error_message)
        return redirect(self.success_url)

class PaqueteDetailView(AdminTecnicoJefeRequiredMixin, DetailView):
    """ Vista para ver los detalles del paquete y sus exámenes """
    model = Paquete
    template_name = 'paquetes/paquete_detalle.html'
    context_object_name = 'paquete'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener todos los exámenes del paquete con sus relaciones y estado en el paquete
        examenes_detalle = PaqueteExamen.objects.filter(
            paquete=self.object,
            estado='Activo'
        ).select_related(
            'examen',
            'examen__categoria', 
            'examen__tipo_muestra'
        ).order_by('orden')
        
        examenes = [detalle.examen for detalle in examenes_detalle]
        context['examenes'] = examenes
        context['examenes_detalle'] = examenes_detalle
        
        # Calcular el total si se compraran individualmente
        total_individual = sum(examen.precio for examen in examenes)
        context['total_individual'] = total_individual
        context['ahorro'] = total_individual - self.object.precio
        
        return context


# ===============================================
# === CRUD para PaqueteExamen (Gestión individual)
# ===============================================

class PaqueteExamenUpdateView(AdminTecnicoJefeRequiredMixin, UpdateView):
    """ Vista para editar un examen individual dentro de un paquete """
    model = PaqueteExamen
    form_class = PaqueteExamenForm
    template_name = 'paquetes/paquete_examen_form.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['titulo'] = f"Editar Examen en Paquete"
        context['paquete'] = self.object.paquete
        context['examen'] = self.object.examen
        return context
    
    def form_valid(self, form):
        messages.success(self.request, "Configuración del examen actualizada exitosamente.")
        super().form_valid(form)
        return redirect(reverse('paquetes:paquete_update', kwargs={'pk': self.object.paquete.pk}))