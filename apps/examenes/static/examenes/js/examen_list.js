document.addEventListener("DOMContentLoaded", function () {
    // 1. Obtener el campo de búsqueda por su ID
    const searchInput = document.getElementById("searchInput");

    // 2. Obtener las filas de la tabla de exámenes por su ID
    // Se ha cambiado de #pacientesTable a #tablaExamenes, que es el ID correcto.
    const tableRows = document.querySelectorAll("#tablaExamenes tbody tr");

    // Verificar si los elementos existen antes de añadir el listener
    if (searchInput && tableRows.length > 0) {
        
        searchInput.addEventListener("keyup", function () {
            // Convertir el valor de búsqueda a minúsculas
            const searchValue = searchInput.value.toLowerCase();

            tableRows.forEach(function (row) {
                // Obtener el texto visible de la fila y convertirlo a minúsculas
                const rowText = row.innerText.toLowerCase();

                // Determinar si la fila contiene el texto buscado
                const isVisible = rowText.includes(searchValue);

                // Mostrar u ocultar la fila
                // Si es visible, el display será la cadena vacía (""), que usa el estilo predeterminado del navegador.
                // Si no es visible, el display será "none".
                row.style.display = isVisible ? "" : "none";
            });
        });
    }
});