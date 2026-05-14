window.onload = function () {

    let username = localStorage.getItem(
        "username"
    );


    if (username) {

        document.getElementById(
            "auth-page"
        ).style.display = "none";


        document.getElementById(
            "app-content"
        ).style.display = "block";


        document.getElementById(
            "current-user"
        ).innerText =
            `Logged in as: ${username}`;


        getPrompts();
    }
}


function showLoginForm(){

    document.getElementById(
        "login-form"
    ).style.display = "block";


    document.getElementById(
        "register-form"
    ).style.display = "none";
}


function showRegisterForm(){

    document.getElementById(
        "register-form"
    ).style.display = "block";


    document.getElementById(
        "login-form"
    ).style.display = "none";
}


async function getPrompts(
    search = "",
    favorites = false
) {

    let token = localStorage.getItem(
        "token"
    );


    let response = await fetch(
        `/api/prompts?search=${search}&favorites=${favorites}`,
        {

            headers: {
                "Authorization": `Bearer ${token}`
            }
        }
    );


    if (!response.ok) {

        return;
    }


    let prompts = await response.json();

    let container = document.getElementById(
        "prompts-container"
    );

    container.innerHTML = "";


    for (let prompt of prompts) {

        container.innerHTML += `

            <div class="prompt">

                <div class="prompt-header">

                    <h2>${prompt.title}</h2>

                    <span
                        class="copy-icon"
                        onclick="copyPrompt('${prompt.content}')"
                    >
                        📋
                    </span>

                </div>

                <p>${prompt.content}</p>

                <small>
                    Category: ${prompt.category}
                </small>

                <br>

                <small>
                    Created:
                    ${new Date(prompt.created_at).toLocaleString()}
                </small>

                <br><br>

                <button onclick="toggleFavorite(${prompt.id})">

                    ${prompt.favorite ? "⭐ Unfavorite" : "☆ Favorite"}

                </button>

                <button onclick="showEditPrompt(${prompt.id})">
                    Edit
                </button>

                <button onclick="deletePrompt(${prompt.id})">
                    Delete
                </button>

            </div>

        `;
    }
}


function searchPrompts(){

    let searchValue = document.getElementById(
        "search"
    ).value;

    getPrompts(searchValue);
}


function showFavorites(){

    getPrompts("", true);
}


function showAllPrompts(){

    getPrompts();
}


async function copyPrompt(content){

    await navigator.clipboard.writeText(content);

    alert("Prompt copied!");
}


async function registerUser(){

    let username = document.getElementById(
        "register-username"
    ).value;


    let password = document.getElementById(
        "register-password"
    ).value;


    let response = await fetch("/api/register", {

        method: "POST",

        headers: {
            "Content-Type": "application/json"
        },

        body: JSON.stringify({

            username: username,

            password: password
        })
    });


    let data = await response.json();


    if (response.ok) {

        alert("Registration successful! Please login.");


        document.getElementById(
            "register-form"
        ).style.display = "none";

    } else {

        alert(data.detail);
    }
}


async function loginUser(){

    let username = document.getElementById(
        "login-username"
    ).value;


    let password = document.getElementById(
        "login-password"
    ).value;


    let formData = new FormData();

    formData.append(
        "username",
        username
    );

    formData.append(
        "password",
        password
    );


    let response = await fetch("/api/login", {

        method: "POST",

        body: formData
    });


    let data = await response.json();


    if (response.ok) {

        localStorage.setItem(
            "token",
            data.access_token
        );


        localStorage.setItem(
            "username",
            username
        );


        document.getElementById(
            "auth-page"
        ).style.display = "none";


        document.getElementById(
            "app-content"
        ).style.display = "block";


        document.getElementById(
            "current-user"
        ).innerText =
            `Logged in as: ${username}`;


        alert("Login successful!");

        getPrompts();

    } else {

        alert(data.detail);
    }
}


function logoutUser(){

    localStorage.removeItem(
        "token"
    );


    localStorage.removeItem(
        "username"
    );


    document.getElementById(
        "auth-page"
    ).style.display = "flex";


    document.getElementById(
        "app-content"
    ).style.display = "none";


    document.getElementById(
        "prompts-container"
    ).innerHTML = "";


    alert("Logged out!");
}


async function createPrompt() {

    let title = document.getElementById("title").value;

    let content = document.getElementById("content").value;

    let category = document.getElementById("category").value;


    if (!title || !content || !category) {

        alert("Please fill all fields");

        return;
    }


    let token = localStorage.getItem(
        "token"
    );


    await fetch("/api/prompts", {

        method: "POST",

        headers: {

            "Content-Type": "application/json",

            "Authorization": `Bearer ${token}`
        },

        body: JSON.stringify({

            title: title,

            content: content,

            category: category
        })
    });


    document.getElementById("title").value = "";

    document.getElementById("content").value = "";

    document.getElementById("category").value = "";


    getPrompts();
}


async function showEditPrompt(id) {

    let updatedData = {};


    let editTitle = confirm(
        "Do you want to edit title?"
    );

    if (editTitle) {

        let newTitle = prompt(
            "Enter new title"
        );

        if (newTitle !== null) {

            updatedData.title = newTitle;
        }
    }


    let editContent = confirm(
        "Do you want to edit content?"
    );

    if (editContent) {

        let newContent = prompt(
            "Enter new content"
        );

        if (newContent !== null) {

            updatedData.content = newContent;
        }
    }


    let editCategory = confirm(
        "Do you want to edit category?"
    );

    if (editCategory) {

        let newCategory = prompt(
            "Enter new category"
        );

        if (newCategory !== null) {

            updatedData.category = newCategory;
        }
    }


    let token = localStorage.getItem(
        "token"
    );


    let response = await fetch(`/api/prompts/${id}`, {

        method: "PATCH",

        headers: {

            "Content-Type": "application/json",

            "Authorization": `Bearer ${token}`
        },

        body: JSON.stringify(updatedData)
    });


    if (response.ok) {

        getPrompts();

    } else {

        alert("Update failed");
    }
}


async function toggleFavorite(id){

    let token = localStorage.getItem(
        "token"
    );


    let response = await fetch(`/api/prompts/${id}`, {

        headers: {
            "Authorization": `Bearer ${token}`
        }
    });

    let prompt = await response.json();


    await fetch(`/api/prompts/${id}`, {

        method: "PATCH",

        headers: {

            "Content-Type": "application/json",

            "Authorization": `Bearer ${token}`
        },

        body: JSON.stringify({

            favorite: !prompt.favorite
        })
    });


    getPrompts();
}


async function deletePrompt(id) {

    let confirmDelete = confirm(
        "Are you sure you want to delete this prompt?"
    );


    if (!confirmDelete) {

        return;
    }


    let token = localStorage.getItem(
        "token"
    );


    await fetch(`/api/prompts/${id}`, {

        method: "DELETE",

        headers: {
            "Authorization": `Bearer ${token}`
        }
    });


    getPrompts();
}