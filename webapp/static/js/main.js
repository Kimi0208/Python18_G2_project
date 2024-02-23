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



    async function onClick(e){
        e.preventDefault()
        let element = e.currentTarget;
        let data_attribute= element.dataset['action_task']
        let response = await makeRequest(data_attribute, "GET")
        let datar = await response.text();
        let modal = document.getElementById('action-task-modal_window')
        modal.innerHTML = datar
        modal.style.display = 'block'
        let form = document.getElementById('test_form');
        form.action = data_attribute
        let closeBtn = document.getElementById("close_modal");
            closeBtn.onclick = function() {
              modal.style.display = "none";
              modal.innerHTML = ''
            }
        }


    function onLoad() {
            let action_buttons = document.getElementsByClassName('action-btn_task')
            for (let action_button of action_buttons) {
                action_button.addEventListener('click', onClick)
            }
        }
    // window.addEventListener('load', onLoad);
    window.addEventListener('load', onLoad);
