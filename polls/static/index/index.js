document.addEventListener("DOMContentLoaded", () => {
    document.querySelector("#nav-ham").addEventListener("click", () => {
        document.querySelector("#sidebar").style.width = "250px";
    })
    document.querySelector("#close-sidebar").addEventListener('click', () => {
        document.querySelector("#sidebar").style.width = "0px";
    })
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
    document.querySelector("#create-contact-form").addEventListener("click", () => {
        const csrf = Cookies.get('csrftoken');
        fetch('/polls/form/create/contact', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(result => {
            window.location = `/polls/form/${result.code}/edit`
        })
    })
    document.querySelector("#create-customer-feedback").addEventListener("click", () => {
        const csrf = Cookies.get('csrftoken');
        fetch('/polls/form/create/feedback', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(result => {
            window.location = `/form/${result.code}/edit`
        })
    })
    document.querySelector("#create-event-registration").addEventListener("click", () => {
        const csrf = Cookies.get('csrftoken');
        fetch('/polls/form/create/event', {
            method: "POST",
            headers: {'X-CSRFToken': csrf},
            body: JSON.stringify({})
        })
        .then(response => response.json())
        .then(result => {
            window.location = `/polls/form/${result.code}/edit`
        })
    })
})