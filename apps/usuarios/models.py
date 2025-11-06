from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from roles.models import Rol  # Importación de la app 'roles'

class Usuario(AbstractUser):
    """
    Modelo de usuario personalizado que hereda de AbstractUser.
    Contiene reglas de negocio para la eliminación.
    """
    # --- CAMPOS ---
    
    # 1. REQUISITO: usuario_id como PK y ordering
    usuario_id = models.AutoField(primary_key=True)
    
    # Anulamos first_name y last_name de AbstractUser para usar los nuestros
    first_name = None
    last_name = None

    email = models.EmailField(unique=True, blank=False, verbose_name="Correo Electrónico")
    nombre = models.CharField(max_length=100, blank=False, verbose_name="Nombres")
    apellido = models.CharField(max_length=100, blank=False, verbose_name="Apellidos")
    dui = models.CharField(max_length=10, unique=True, blank=False, verbose_name="DUI")
    estado = models.CharField(
        max_length=20,
        default='Activo',
        choices=[('Activo', 'Activo'), ('Inactivo', 'Inactivo')],
        blank=False
    )
    
    # 2. REQUISITO: Rol puede ser nulo
    rol = models.ForeignKey(
        Rol, 
        on_delete=models.PROTECT, # PROTECT para que la BBDD también lo impida
        null=True, 
        blank=True,
        verbose_name="Rol de Usuario"
    )

    # --- CONFIGURACIÓN ---
    
    USERNAME_FIELD = 'username'
    # 'email', 'nombre', 'apellido', 'dui' son requeridos para superusuario
    REQUIRED_FIELDS = ['email', 'nombre', 'apellido', 'dui']

    def __str__(self):
        return f"{self.nombre} {self.apellido} ({self.username})"

    # --- REGLAS DE NEGOCIO (MOVIDAS AL MODELO) ---
    
    def puede_eliminarse(self):
        """
        Verifica si el usuario puede ser eliminado según las reglas de negocio.
        Devuelve (True, None) si se puede, o (False, "Mensaje de error") si no.
        """
        # Regla 1: No se puede eliminar a un superusuario.
        if self.is_superuser:
            return (False, f"No se puede eliminar al superusuario '{self.username}'.")
        
        # Regla 2: No se puede eliminar al ÚNICO administrador del sistema.
        if self.rol and self.rol.nombre == 'Administrador':
            admin_count = Usuario.objects.filter(rol__nombre='Administrador', estado='Activo').count()
            if admin_count <= 1:
                return (False, "No se puede eliminar al único administrador activo del sistema.")
                
        # Regla 3 (Implícita por on_delete=models.PROTECT): 
        # Si tiene otros objetos relacionados que lo protegen, la BBDD lanzará ProtectedError.
        
        return (True, None)

    def delete(self, *args, **kwargs):
        """
        Sobrescribe el método de eliminación para aplicar reglas de negocio.
        """
        se_puede, razon = self.puede_eliminarse()
        
        if not se_puede:
            raise ValidationError(razon)
            
        super().delete(*args, **kwargs)

    def clean(self):
        """
        Reglas de integridad de datos.
        """
        # Regla: Si es superusuario, forzar estado Activo, is_staff y Rol de Admin.
        if self.is_superuser:
            self.is_staff = True
            self.estado = 'Activo'
            try:
                admin_rol = Rol.objects.get(nombre='Administrador')
                self.rol = admin_rol
            except Rol.DoesNotExist:
                # Si el rol 'Administrador' no existe, se generará un error
                # al intentar guardar, lo cual es correcto.
                pass
        super().clean()

    def save(self, *args, **kwargs):
        self.full_clean()  # Llama a clean() antes de guardar
        super().save(*args, **kwargs)

    # 3. REQUISITO: Añadir Meta, igual que en Roles
    class Meta:
        db_table = 'Usuarios'
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['usuario_id']