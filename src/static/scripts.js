document.getElementById("search-form").addEventListener("submit", async (event) => {
    event.preventDefault();

    const query = document.getElementById("query").value;
    const resultsDiv = document.getElementById("results");
    resultsDiv.innerHTML = "<p>Buscando...</p>";

    try {
        const response = await fetch("/search", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ query: query }),
        });

        if (!response.ok) {
            throw new Error("Error en la búsqueda");
        }

        const data = await response.json();
        resultsDiv.innerHTML = "";

        if (data.results.length === 0) {
            resultsDiv.innerHTML = "<p>No se encontraron resultados</p>";
            return;
        }

        const resultsList = document.createElement("ul");
        data.results.forEach((result) => {
            const item = document.createElement("li");
            item.textContent = `Propuesta: ${result["Solucion Propuesta"]}, Número: ${result["Numero de Incidencia"]}, Prioridad: ${result["Prioridad"]}`;
            resultsList.appendChild(item);
        });
        resultsDiv.appendChild(resultsList);
    } catch (error) {
        resultsDiv.innerHTML = `<p>Error: ${error.message}</p>`;
    }
});
