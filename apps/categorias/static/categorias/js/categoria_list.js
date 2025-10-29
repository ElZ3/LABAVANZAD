document.addEventListener("DOMContentLoaded", function () {
    const searchInput = document.getElementById("searchInput");
    // Apunta a la tabla de categorías: #tablaCategorias
    const tableRows = document.querySelectorAll("#tablaCategorias tbody tr"); 

    if (searchInput && tableRows.length > 0) {
        
        searchInput.addEventListener("keyup", function () {
            const searchValue = searchInput.value.toLowerCase();

            tableRows.forEach(function (row) {
                const rowText = row.innerText.toLowerCase();
                const isVisible = rowText.includes(searchValue);
                row.style.display = isVisible ? "" : "none";
            });
        });
    }
});