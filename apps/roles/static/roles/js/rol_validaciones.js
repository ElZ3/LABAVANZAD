// ======================= VALIDACIONES DE FORMULARIO DE ROLES =======================

// PATRONES SINCRONIZADOS (se asignan dinámicamente desde Django)
const REGEX_PATTERNS = {
    nombre: new RegExp(window.regexPatterns?.nombre || ".*"),
    descripcion: new RegExp(window.regexPatterns?.descripcion || ".*"),
};

const ERROR_MESSAGES = {
    nombre: window.errorMessages?.nombre || "Formato inválido para nombre",
    descripcion: window.errorMessages?.descripcion || "Formato inválido para descripción",
    campo_vacio: window.errorMessages?.campo_vacio || "Este campo es requerido",
};


// Variable global para controlar notificaciones de errores
let notificacionMostrada = {
    nombre: false,
    descripcion: false
};

// --------------------------- Inicialización ---------------------------
document.addEventListener('DOMContentLoaded', function() {
    configurarValidacionEnTiempoReal();
    mostrarErroresServidor();
});

// --------------------------- Configuración ---------------------------
function configurarValidacionEnTiempoReal() {
    const form = document.querySelector('form');
    const campos = ['nombre', 'descripcion'];
    
    campos.forEach(campoNombre => {
        const campo = document.getElementById(`id_${campoNombre}`);
        if (campo) {
            campo.addEventListener('blur', function() {
                notificacionMostrada[this.name] = false;
                validarCampoIndividual(this);
            });
        }
    });
    
    if (form) {
        form.addEventListener('submit', function(e) {
            Object.keys(notificacionMostrada).forEach(key => {
                notificacionMostrada[key] = false;
            });
            
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
    
    if (!valor) {
        mostrarErrorCampo(campo, ERROR_MESSAGES.campo_vacio);
        return false;
    }
    
    if (REGEX_PATTERNS[nombreCampo] && !REGEX_PATTERNS[nombreCampo].test(valor)) {
        mostrarErrorCampo(campo, ERROR_MESSAGES[nombreCampo]);
        return false;
    }
    
    campo.classList.add('is-valid');
    return true;
}

function validarFormularioCompleto() {
    let esValido = true;
    const campos = ['nombre', 'descripcion'];
    
    campos.forEach(campoNombre => {
        const campo = document.getElementById(`id_${campoNombre}`);
        if (campo && !validarCampoIndividual(campo)) {
            esValido = false;
        }
    });
    
    return esValido;
}

// --------------------------- Errores ---------------------------
function mostrarErrorCampo(campo, mensaje) {
    const nombreCampo = campo.name;
    
    campo.classList.remove('is-valid');
    campo.classList.add('is-invalid');
    
    if (!notificacionMostrada[nombreCampo]) {
        notificacionMostrada[nombreCampo] = true;
    }
    
    let errorElement = campo.parentNode.querySelector('.invalid-feedback');
    if (!errorElement) {
        errorElement = document.createElement('div');
        errorElement.className = 'invalid-feedback';
        campo.parentNode.appendChild(errorElement);
    }
    
    if (errorElement.textContent !== mensaje) {
        errorElement.textContent = mensaje;
    }
}

function limpiarErrorCampo(campo) {
    const nombreCampo = campo.name;
    campo.classList.remove('is-invalid');
    
    if (campo.value.trim()) {
        campo.classList.add('is-valid');
    }
    
    notificacionMostrada[nombreCampo] = false;
    
    const errorElement = campo.parentNode.querySelector('.invalid-feedback');
    if (errorElement) {
        errorElement.textContent = '';
    }
}

// --------------------------- Errores del Servidor ---------------------------
function mostrarErroresServidor() {
    if (window.serverErrors && Array.isArray(window.serverErrors)) {
        window.serverErrors.forEach(error => {
            mostrarNotificacionError(error);
        });
    }
}
