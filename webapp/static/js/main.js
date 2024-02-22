
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
            return await response.json();
        } else {
            let error = new Error(response.statusText);
            error.response = response;
            throw error;
        }

    }


    async function onClick(e){
        e.preventDefault()
        let element = e.currentTarget;
        let data_attribute= element.dataset['task_action']
        console.log(data_attribute)
        let token = localStorage.getItem('apiToken');
        let form = document.getElementById('create-task-form');

        let title = form.elements['title'].value;
        let description = form.elements['description'].value;
        let data = {"title": title, "description": description}
        console.log(data)
        console.log(token)

        let rrr = await makeRequest(`http://127.0.0.1:8000/api/tasks/`, data_attribute, data, token)
        console.log(rrr)
        // modal.style.display = "none"
    }

    async function onTest(e){
        e.preventDefault()
        let response = await fetch('http://127.0.0.1:8000/create/')
        let data = await response.text();
        let modal = document.getElementById('create-task-modal_window')
        modal.innerHTML += data
        modal.style.display = 'block'
        let form = document.getElementById('test_test');
        let title = form.elements['title'].value;
        let description = form.elements['description'].value;
        console.log(title)
        console.log(description)
        send_data = document.getElementById('send_data')
        send_data.preventDefault()
        // let data2 = {"title": title, "description": description}
        // let pr = await makeRequest('http://127.0.0.1:8000/create/', "POST", data2, token)
        }




    function onLoad() {
            let button = document.getElementById('button_create_task');
                button.addEventListener('click', onClick)
            let jerry = document.getElementById('tom')
            jerry.addEventListener('click', onTest)
        }
    let createBtn = document.getElementById("create-task-btn");
    let modal = document.getElementById("create-task-modal");

    createBtn.onclick = function() {
      modal.style.display = "block";
    }

    let closeBtn = modal.getElementsByClassName("close")[0];
    closeBtn.onclick = function() {
      modal.style.display = "none";
    }

    window.onclick = function(event) {
      if (event.target == modal) {
        modal.style.display = "none";
      }
    }
    window.addEventListener('load', onLoad);