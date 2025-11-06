// ======================= VALIDACIONES DE FORMULARIO DE ORDEN (CREAR) =======================
// (Valida el formulario 'orden_form_crear.html')

const ERROR_MESSAGES = {
    seleccion_vacia: "Debes seleccionar una opción.",
};

// Campos del formulario DE CREACIÓN a validar
const CAMPOS_A_VALIDAR = ['paciente', 'prioridad', 'metodo_entrega']; // Convenio es opcional

// --------------------------- Inicialización ---------------------------
document.addEventListener('DOMContentLoaded', function() {
    configurarValidacionEnTiempoReal();
});

// --------------------------- Configuración ---------------------------
function configurarValidacionEnTiempoReal() {
    const form = document.getElementById('ordenCreateForm');
    if (!form) return; // Solo se aplica al formulario de creación
    
    CAMPOS_A_VALIDAR.forEach(campoNombre => {
        const campo = document.getElementById(`id_${campoNombre}`);
        if (campo) {
            campo.addEventListener('change', function() {
                validarCampoIndividual(this);
            });
        }
    });
    
    form.addEventListener('submit', function(e) {
        if (!validarFormularioCompleto()) {
            e.preventDefault();
        }
    });
}

// --------------------------- Validaciones ---------------------------
function validarCampoIndividual(campo) {
    let valor = campo.value;
    limpiarErrorCampo(campo);

    if (!valor) {
        mostrarErrorCampo(campo, ERROR_MESSAGES.seleccion_vacia);
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
    return esValido;
}

// --------------------------- Funciones Auxiliares (Errores) ---------------------------
function mostrarErrorCampo(campo, mensaje) {
    campo.classList.remove('is-valid');
    campo.classList.add('is-invalid');
    // Asumimos que el div de error está presente en el HTML
    const errorElement = campo.parentNode.querySelector('.text-danger.small');
    if (errorElement) {
        errorElement.textContent = mensaje;
    }
}

function limpiarErrorCampo(campo) {
    campo.classList.remove('is-invalid');
    const errorElement = campo.parentNode.querySelector('.text-danger.small');
    if (errorElement) {
        errorElement.textContent = '';
    }
}