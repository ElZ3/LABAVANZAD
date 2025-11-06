// ======================= VALIDACIONES DE FORMULARIO DE USUARIO =======================

// Patrones y Mensajes (se llenan desde el template de Django)
const REGEX_PATTERNS = {
    username: new RegExp(window.regexPatterns?.username || ".*"),
    nombre: new RegExp(window.regexPatterns?.nombre || ".*"),
    apellido: new RegExp(window.regexPatterns?.apellido || ".*"),
    dui: new RegExp(window.regexPatterns?.dui || ".*"),
    email: new RegExp(window.regexPatterns?.email || ".*"),
};

const ERROR_MESSAGES = {
    username: window.errorMessages?.username || "Formato de username inválido.",
    nombre: window.errorMessages?.nombre || "Formato de nombre inválido.",
    apellido: window.errorMessages?.apellido || "Formato de apellido inválido.",
    dui: window.errorMessages?.dui || "Formato de DUI inválido.",
    campo_vacio: window.errorMessages?.campo_vacio || "Este campo es requerido.",
    email_invalido: window.errorMessages?.email_invalido || "Email inválido.",
};

// Campos que requieren validación de formato
const CAMPOS_A_VALIDAR = ['username', 'nombre', 'apellido', 'dui', 'email'];

// --------------------------- Inicialización ---------------------------
document.addEventListener('DOMContentLoaded', function() {
    configurarValidacionEnTiempoReal();
    configurarToggleContrasena();
    // mostrarErroresServidor(); // Puedes descomentar si lo necesitas
});

// --------------------------- Configuración ---------------------------
function configurarValidacionEnTiempoReal() {
    const form = document.getElementById('usuarioForm');
    
    CAMPOS_A_VALIDAR.forEach(campoNombre => {
        const campo = document.getElementById(`id_${campoNombre}`);
        if (campo) {
            campo.addEventListener('blur', function() {
                validarCampoIndividual(this);
            });
            campo.addEventListener('input', function() {
                // Opcional: limpiar error al escribir
                if (this.classList.contains('is-invalid')) {
                    limpiarErrorCampo(this);
                }
            });
        }
    });
    
    if (form) {
        form.addEventListener('submit', function(e) {
            if (!validarFormularioCompleto()) {
                e.preventDefault();
                // Opcional: mostrar un mensaje general
                // mostrarNotificacionError("Por favor, corrige los errores en el formulario.");
            }
        });
    }
}

/**
 * REQUISITO: Configura los botones de "mostrar/ocultar" contraseña.
 */
function configurarToggleContrasena() {
    document.querySelectorAll('.toggle-password').forEach(button => {
        button.addEventListener('click', function() {
            const targetId = this.getAttribute('data-target');
            const passwordInput = document.getElementById(targetId);
            const icon = this.querySelector('i');

            if (passwordInput) {
                if (passwordInput.type === 'password') {
                    passwordInput.type = 'text';
                    icon.classList.remove('fa-eye');
                    icon.classList.add('fa-eye-slash');
                } else {
                    passwordInput.type = 'password';
                    icon.classList.remove('fa-eye-slash');
                    icon.classList.add('fa-eye');
                }
            }
        });
    });
}

// --------------------------- Validaciones ---------------------------

function validarCampoIndividual(campo) {
    const valor = campo.value.trim();
    const nombreCampo = campo.name;
    
    limpiarErrorCampo(campo);

    // 1. Validación de campo vacío
    if (!valor) {
        if (nombreCampo !== 'rol') { // Rol puede ser opcional
             mostrarErrorCampo(campo, ERROR_MESSAGES.campo_vacio);
             return false;
        }
    }

    // 2. Validación de formato (Otros campos)
    else if (REGEX_PATTERNS[nombreCampo] && !REGEX_PATTERNS[nombreCampo].test(valor)) {
        mostrarErrorCampo(campo, ERROR_MESSAGES[nombreCampo]);
        return false;
    }
    
    campo.classList.add('is-valid');
    return true;
}

function validarFormularioCompleto() {
    let esValido = true;
    CAMPOS_A_VALIDAR.forEach(campoNombre => {
        const campo = document.getElementById(`id_${campoNombre}`);
        if (campo && !validarCampoIndividual(campo)) {
            esValido = false;
        }
    });
    
    // Aquí puedes añadir validación de contraseñas si es necesario
    // (ej. 'password' y 'password2' en el formulario de registro)
    
    return esValido;
}

// --------------------------- Funciones Auxiliares (Errores) ---------------------------

function mostrarErrorCampo(campo, mensaje) {
    campo.classList.remove('is-valid');
    campo.classList.add('is-invalid');
    
    let errorElement = campo.parentNode.querySelector('.invalid-feedback');
    if (!errorElement) {
        // Si el campo está en un 'input-group' (como la contraseña)
        const parent = campo.closest('.input-group') || campo.parentNode;
        errorElement = parent.parentNode.querySelector('.invalid-feedback');
    }
    
    if (errorElement) {
        errorElement.textContent = mensaje;
    }
}

function limpiarErrorCampo(campo) {
    campo.classList.remove('is-invalid');
    
    // No añadir 'is-valid' automáticamente al limpiar, 
    // solo después de una validación exitosa (en validarCampoIndividual)
    
    let errorElement = campo.parentNode.querySelector('.invalid-feedback');
    if (!errorElement) {
        const parent = campo.closest('.input-group') || campo.parentNode;
        errorElement = parent.parentNode.querySelector('.invalid-feedback');
    }
    
    if (errorElement) {
        errorElement.textContent = '';
    }
}