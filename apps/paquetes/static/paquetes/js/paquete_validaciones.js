// ======================= VALIDACIONES DE FORMULARIO DE PAQUETE =======================
const REGEX_PATTERNS = {
    nombre: new RegExp(window.regexPatterns?.nombre || ".*"),
};
const ERROR_MESSAGES = {
    nombre: window.errorMessages?.nombre || "Formato de nombre inválido.",
    precio: window.errorMessages?.precio || "Precio inválido.",
    campo_vacio: window.errorMessages?.campo_vacio || "Este campo es requerido.",
};

const CAMPOS_A_VALIDAR = ['nombre', 'precio', 'estado', 'examenes'];

document.addEventListener('DOMContentLoaded', function() {
    configurarValidacionEnTiempoReal();
    configurarResumenExamenes();
});

function configurarValidacionEnTiempoReal() {
    const form = document.getElementById('paqueteForm');
    if (!form) return;

    CAMPOS_A_VALIDAR.forEach(campoNombre => {
        const campo = document.getElementById(`id_${campoNombre}`);
        if (campo) {
            const eventType = (campo.tagName.toLowerCase() === 'select' || campo.multiple) ? 'change' : 'blur';
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

function configurarResumenExamenes() {
    const selectExamenes = document.getElementById('id_examenes');
    const resumenDiv = document.getElementById('resumenExamenes');
    const listaDiv = document.getElementById('listaExamenes');

    if (selectExamenes && resumenDiv && listaDiv) {
        selectExamenes.addEventListener('change', function() {
            const seleccionados = Array.from(this.selectedOptions);
            
            if (seleccionados.length > 0) {
                listaDiv.innerHTML = seleccionados.map(option => 
                    `<span class="badge bg-secondary me-1 mb-1">${option.text}</span>`
                ).join('');
                resumenDiv.classList.remove('d-none');
            } else {
                resumenDiv.classList.add('d-none');
            }
        });

        // Ejecutar una vez al cargar para mostrar selección actual
        const event = new Event('change');
        selectExamenes.dispatchEvent(event);
    }
}

function validarCampoIndividual(campo) {
    let valor = campo.value;
    const nombreCampo = campo.name;

    if (campo.type !== 'select-one' && !campo.multiple) {
        valor = valor.trim();
    }

    limpiarErrorCampo(campo);

    // Validación de campo vacío
    if (!valor || (campo.multiple && campo.selectedOptions.length === 0)) {
        const mensaje = (campo.multiple) 
            ? "Debe seleccionar al menos un examen."
            : ERROR_MESSAGES.campo_vacio;
        mostrarErrorCampo(campo, mensaje);
        return false;
    }

    // Validación de regex para nombre
    if (nombreCampo === 'nombre' && REGEX_PATTERNS[nombreCampo]) {
        if (!REGEX_PATTERNS[nombreCampo].test(valor)) {
            mostrarErrorCampo(campo, ERROR_MESSAGES[nombreCampo]);
            return false;
        }
    }

    // Validación de precio
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
        if (campo.tagName.toLowerCase() === 'select' || campo.multiple) {
            errorElement.classList.add('d-block');
        }
        errorElement.textContent = mensaje;
    }
}

function limpiarErrorCampo(campo) {
    campo.classList.remove('is-invalid');
    
    const errorElement = campo.parentNode.querySelector('.invalid-feedback');
    if (errorElement) {
        if (campo.tagName.toLowerCase() === 'select' || campo.multiple) {
            errorElement.classList.remove('d-block');
        }
        errorElement.textContent = '';
    }
}