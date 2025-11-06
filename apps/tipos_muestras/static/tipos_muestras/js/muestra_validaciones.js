// ======================= VALIDACIONES DE FORMULARIO DE TIPO DE MUESTRA =======================

// Patrones y Mensajes (se llenan desde el template de Django)
const REGEX_PATTERNS = {
    nombre: new RegExp(window.regexPatterns?.nombre || ".*"),
    descripcion: new RegExp(window.regexPatterns?.general || ".*"), // Usa el regex 'general'
    condiciones_almacenamiento: new RegExp(window.regexPatterns?.general || ".*"), // Usa el regex 'general'
};

const ERROR_MESSAGES = {
    nombre: window.errorMessages?.nombre || "Formato de nombre inválido.",
    descripcion: window.errorMessages?.descripcion || "Formato de descripción inválido.",
    condiciones_almacenamiento: window.errorMessages?.condiciones_almacenamiento || "Formato de condiciones inválido.",
    campo_vacio: window.errorMessages?.campo_vacio || "Este campo es requerido.",
};

// Campos a validar por el JS
const CAMPOS_A_VALIDAR = ['nombre', 'descripcion', 'condiciones_almacenamiento'];

// --------------------------- Inicialización ---------------------------
document.addEventListener('DOMContentLoaded', function() {
    configurarValidacionEnTiempoReal();
});

// --------------------------- Configuración ---------------------------
function configurarValidacionEnTiempoReal() {
    const form = document.getElementById('muestraForm');
    
    CAMPOS_A_VALIDAR.forEach(campoNombre => {
        const campo = document.getElementById(`id_${campoNombre}`);
        if (campo) {
            campo.addEventListener('blur', function() {
                validarCampoIndividual(this);
            });
            campo.addEventListener('input', function() {
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
            }
        });
    }
}

// --------------------------- Validaciones ---------------------------

function validarCampoIndividual(campo) {
    const valor = campo.value.trim();
    const nombreCampo = campo.name;
    
    limpiarErrorCampo(campo);

    // 1. Validación de campo vacío
    if (!valor) {
        mostrarErrorCampo(campo, ERROR_MESSAGES.campo_vacio);
        return false;
    }

    // 2. Validación de formato
    if (REGEX_PATTERNS[nombreCampo]) {
        if (!REGEX_PATTERNS[nombreCampo].test(valor)) {
            mostrarErrorCampo(campo, ERROR_MESSAGES[nombreCampo]);
            return false;
        }
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
    return esValido;
}

// --------------------------- Funciones Auxiliares (Errores) ---------------------------

function mostrarErrorCampo(campo, mensaje) {
    campo.classList.remove('is-valid');
    campo.classList.add('is-invalid');
    
    const errorElement = campo.parentNode.querySelector('.invalid-feedback');
    if (errorElement) {
        errorElement.textContent = mensaje;
    }
}

function limpiarErrorCampo(campo) {
    campo.classList.remove('is-invalid');
    
    const errorElement = campo.parentNode.querySelector('.invalid-feedback');
    if (errorElement) {
        errorElement.textContent = '';
    }
}