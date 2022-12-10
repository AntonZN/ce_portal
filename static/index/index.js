document.addEventListener("DOMContentLoaded", () => {


    document.querySelector("#create-blank-form").addEventListener("click", () => {
        const csrf = Cookies.get('csrftoken');
        fetch('/polls/form/create', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({
                title: "Название формы"
            })
        })
        .then(response => response.json())
        .then(result => {
            window.location = `/polls/form/${result.code}/edit`
        })
    })



})