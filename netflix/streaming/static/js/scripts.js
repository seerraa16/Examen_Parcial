// scripts.js

function addToMyList(movieId) {
    fetch("/add-to-my-list/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({ movie_id: movieId })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error("Error al añadir la película.");
        }
        return response.json();
    })
    .then(data => {
        if (data.success) {
            alert("Película añadida a tu lista");
        } else {
            alert(data.message);
        }
    })
    .catch(error => console.error("Error:", error));
}
