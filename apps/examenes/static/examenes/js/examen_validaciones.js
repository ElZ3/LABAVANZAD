// ======================= VALIDACIONES DE FORMULARIO DE EXAMEN (PRINCIPAL) =======================
const REGEX_PATTERNS = {
    nombre: new RegExp(window.regexPatterns?.nombre || ".*"),
    codigo: new RegExp(window.regexPatterns?.codigo || ".*"),
};
const ERROR_MESSAGES = {
    nombre: window.errorMessages?.nombre || "Formato de nombre inválido.",
    codigo: window.errorMessages?.codigo || "Formato de código inválido.",
    precio: window.errorMessages?.precio || "Precio inválido.",
    campo_vacio: window.errorMessages?.campo_vacio || "Este campo es requerido.",
    seleccion_vacia: window.errorMessages?.seleccion_vacia || "Selección requerida.",
};
// No necesitamos validar los formularios de hijos aquí
const CAMPOS_A_VALIDAR = ['nombre', 'codigo', 'precio', 'categoria', 'tipo_muestra', 'estado'];
document.addEventListener('DOMContentLoaded', function() {
    configurarValidacionEnTiempoReal();
});
function configurarValidacionEnTiempoReal() {
    const form = document.getElementById('examenForm');
    if (!form) return; // Salir si no estamos en el form de examen
    
    CAMPOS_A_VALIDAR.forEach(campoNombre => {
        const campo = document.getElementById(`id_${campoNombre}`);
        if (campo) {
            const eventType = (campo.tagName.toLowerCase() === 'select') ? 'change' : 'blur';
            campo.addEventListener(eventType, function() {
                validarCampoIndividual(this);
            });
            if (eventType !== 'change') {
                campo.addEventListener('input', () => limpiarErrorCampo(campo));
            }
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
function validarCampoIndividual(campo) {
    let valor = campo.value;
    const nombreCampo = campo.name;
    if (campo.type !== 'select-one') {
        valor = valor.trim();
    }
    if (nombreCampo === 'codigo') {
        campo.value = valor.toUpperCase();
        valor = campo.value;
    }
    limpiarErrorCampo(campo);
    if (!valor) {
        const mensaje = (campo.tagName.toLowerCase() === 'select') 
            ? ERROR_MESSAGES.seleccion_vacia 
            : ERROR_MESSAGES.campo_vacio;
        mostrarErrorCampo(campo, mensaje);
        return false;
    }
    if (REGEX_PATTERNS[nombreCampo]) {
        if (!REGEX_PATTERNS[nombreCampo].test(valor)) {
            mostrarErrorCampo(campo, ERROR_MESSAGES[nombreCampo]);
            return false;
        }
    }
    if (nombreCampo === 'precio') {
        if (parseFloat(valor) <= 0) {
            mostrarErrorCampo(campo, ERROR_MESSAGES.precio);
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
function mostrarErrorCampo(campo, mensaje) {
    campo.classList.remove('is-valid');
    campo.classList.add('is-invalid');
    const errorElement = campo.parentNode.querySelector('.invalid-feedback');
    if (errorElement) {
        if(campo.tagName.toLowerCase() === 'select') {
            errorElement.classList.add('d-block');
        }
        errorElement.textContent = mensaje;
    }
}
function limpiarErrorCampo(campo) {
    campo.classList.remove('is-invalid');
    const errorElement = campo.parentNode.querySelector('.invalid-feedback');
    if (errorElement) {
        if(campo.tagName.toLowerCase() === 'select') {
            errorElement.classList.remove('d-block');
        }
        errorElement.textContent = '';
    }
}