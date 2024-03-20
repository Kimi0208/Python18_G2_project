async function makeRequest(url, method = 'GET', data = null, token = null) {
    let headers = {
        "Content-Type": "application/json"
    };
    if (token) {
        headers['Authorization'] = 'Token ' + token;

    }
    let options;

    if (method !== "GET") {
        options = {method, headers, body: JSON.stringify(data),};
    } else {
        options = {method, headers};
    }
    let response = await fetch(url, options);

    if (response.ok) {
        let contentType = response.headers.get("content-type");
        if (contentType && contentType.includes("application/json")) {
            return await response.json();
        } else {
            return response;
        }
    } else {
        let error = new Error(response.statusText);
        error.response = response;
        throw error;
    }
}


async function onClick(e) {
    e.preventDefault()


}


function onLoad() {
    let action_buttons = document.getElementById('submit_button')
    console.log(action_buttons)
    action_buttons.addEventListener('click', onClick)
}

window.addEventListener('load', onLoad);


export {onLoad, makeRequest, onClick};