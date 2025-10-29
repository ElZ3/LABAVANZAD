document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    // Apunta a la tabla correcta: #tablaPacientes
    const tableRows = document.querySelectorAll("#tablaPacientes tbody tr"); 

    if (searchInput && tableRows.length > 0) {
        
        searchInput.addEventListener("keyup", function () {
            const searchValue = searchInput.value.toLowerCase();

            tableRows.forEach(function (row) {
                // Obtiene todo el texto de la fila (Nombre, DUI, Teléfono, Correo)
                const rowText = row.innerText.toLowerCase();
                const isVisible = rowText.includes(searchValue);
                
                // Muestra u oculta la fila
                row.style.display = isVisible ? "" : "none";
            });
        });
    }
});