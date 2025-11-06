// ======================= FUNCIONALIDAD LISTA DE PAQUETES =======================
document.addEventListener('DOMContentLoaded', function() {
    const searchInput = document.getElementById('searchInput');
    const tabla = document.getElementById('tablaPaquetes');
    const deleteButtons = document.querySelectorAll('.delete-btn');

    // Búsqueda en tiempo real
    if (searchInput && tabla) {
        searchInput.addEventListener('input', function() {
            const filter = this.value.toLowerCase();
            const rows = tabla.getElementsByTagName('tbody')[0].getElementsByTagName('tr');
            
            Array.from(rows).forEach(row => {
                const text = row.textContent.toLowerCase();
                row.style.display = text.includes(filter) ? '' : 'none';
            });
        });
    }

    // Confirmación de eliminación
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            const nombrePaquete = this.getAttribute('data-nombre');
            if (!confirm(`¿Está seguro de que desea eliminar el paquete "${nombrePaquete}"?`)) {
                e.preventDefault();
            }
        });
    });

    // Ordenamiento de tabla
    const headers = tabla.querySelectorAll('thead th');
    headers.forEach((header, index) => {
        header.style.cursor = 'pointer';
        header.addEventListener('click', function() {
            sortTable(index);
        });
    });

    function sortTable(columnIndex) {
        const tbody = tabla.querySelector('tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));
        const isNumeric = columnIndex === 0 || columnIndex === 3 || columnIndex === 4; // #, Precio, Exámenes

        rows.sort((a, b) => {
            let aValue = a.cells[columnIndex].textContent.trim();
            let bValue = b.cells[columnIndex].textContent.trim();

            if (isNumeric) {
                aValue = parseFloat(aValue.replace(/[^0-9.-]+/g, "")) || 0;
                bValue = parseFloat(bValue.replace(/[^0-9.-]+/g, "")) || 0;
                return aValue - bValue;
            } else {
                return aValue.localeCompare(bValue);
            }
        });

        // Limpiar y reinsertar filas ordenadas
        while (tbody.firstChild) {
            tbody.removeChild(tbody.firstChild);
        }
        rows.forEach(row => tbody.appendChild(row));
    }
});