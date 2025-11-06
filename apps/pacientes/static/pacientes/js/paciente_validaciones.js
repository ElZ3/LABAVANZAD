// ======================= VALIDACIONES DE FORMULARIO DE PACIENTE =======================

// Patrones y Mensajes (se llenan desde el template de Django)
const REGEX_PATTERNS = {
    nombre: new RegExp(window.regexPatterns?.nombre || ".*"),
    apellido: new RegExp(window.regexPatterns?.apellido || ".*"),
    dui: new RegExp(window.regexPatterns?.dui || ".*"),
    telefono: new RegExp(window.regexPatterns?.telefono || ".*"),
    correo: new RegExp(window.regexPatterns?.correo || ".*"),
};

const ERROR_MESSAGES = {
    nombre: window.errorMessages?.nombre || "Formato de nombre inválido.",
    apellido: window.errorMessages?.apellido || "Formato de apellido inválido.",
    dui: window.errorMessages?.dui || "Formato de DUI inválido.",
    telefono: window.errorMessages?.telefono || "Teléfono debe tener 8 dígitos.",
    correo: window.errorMessages?.correo || "Correo inválido.",
    campo_vacio: window.errorMessages?.campo_vacio || "Este campo es requerido.",
    seleccion_vacia: window.errorMessages?.seleccion_vacia || "Debe seleccionar una opción.",
};

// Todos los campos en este formulario son requeridos y deben validarse
const CAMPOS_A_VALIDAR = [
    'nombre', 'apellido', 'fecha_nacimiento', 'sexo',
    'dui', 'telefono', 'correo'
];

// --------------------------- Inicialización ---------------------------
document.addEventListener('DOMContentLoaded', function() {
    configurarValidacionEnTiempoReal();
});

// --------------------------- Configuración ---------------------------
function configurarValidacionEnTiempoReal() {
    const form = document.getElementById('pacienteForm');
    
    CAMPOS_A_VALIDAR.forEach(campoNombre => {
        const campo = document.getElementById(`id_${campoNombre}`);
        if (campo) {
            // Validar al perder el foco
            campo.addEventListener('blur', function() {
                validarCampoIndividual(this);
            });
            // Limpiar error al escribir
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
                // Opcional: mostrar un mensaje general
            }
        });
    }
}

// --------------------------- Validaciones ---------------------------

function validarCampoIndividual(campo) {
    let valor = campo.value;
    const nombreCampo = campo.name;
    
    // Limpiar espacios en blanco, excepto para 'sexo' o 'fecha_nacimiento'
    if (campo.type !== 'select-one' && campo.type !== 'date') {
        valor = valor.trim();
    }
    
    // Caso especial: teléfono (limpiar guiones/espacios para validar)
    if (nombreCampo === 'telefono') {
        valor = valor.replace(/[\s\-]/g, '');
        campo.value = valor; // Actualizar el campo con el valor limpio
    }

    limpiarErrorCampo(campo);

    // 1. Validación de campo vacío
    if (!valor) {
        const mensaje = (campo.type === 'select-one') 
            ? ERROR_MESSAGES.seleccion_vacia 
            : ERROR_MESSAGES.campo_vacio;
        mostrarErrorCampo(campo, mensaje);
        return false;
    }

    // 2. Validación de formato (si aplica)
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
    
    // Añadir 'is-valid' solo si el campo tiene contenido después de limpiar
    if (campo.value.trim() && campo.type !== 'select-one' && campo.type !== 'date') {
         // No marcamos como válido al instante, solo al validar
    }
    
    const errorElement = campo.parentNode.querySelector('.invalid-feedback');
    if (errorElement) {
        errorElement.textContent = '';
    }
}