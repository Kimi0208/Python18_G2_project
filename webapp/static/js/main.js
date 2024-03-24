async function makeRequest(url, method = 'GET', data = null, token = null) {
    let headers = {
        "Content-Type": "application/json"
    };
    if (token) {
        headers['Authorization'] = 'Token ' + token;

    }
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    headers['X-CSRFToken'] = csrftoken;
    let options;

    if (method !== "GET") {
        options = {method, headers, body: JSON.stringify(data),};
    } else {
        options = {method, headers};
    }
    console.log(url)
    console.log(options)
    let response = await fetch(url, options);
    console.log(response)
    console.log(response.headers.get('content-type'))

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
    let element = e.currentTarget;
    let data_attribute = element.dataset['action_task']
    let response = await makeRequest(data_attribute, "GET")
    let datar = await response.text();
    let modal = document.getElementById('action-task-modal_window')
    modal.innerHTML = datar
    modal.style.display = 'block'
    let form = document.getElementById('test_form');
    form.addEventListener('submit', onSubmitData)
    form.action = data_attribute
    let closeBtn = document.getElementById("close_modal");
    closeBtn.onclick = function () {
        modal.style.display = "none";
        modal.innerHTML = ''
    }
}

async function onSubmitData(e) {
    e.preventDefault();
    let form = e.target.closest('form');
    let title = form.elements['title'].value;
    let type = form.elements['type'].value
    let description = form.elements['description'].value;
    let start_date = form.elements['start_date'].value
    let done_at = form.elements['done_at'].value
    let deadline = form.elements['deadline'].value
    let status = form.elements['status'].value
    let priority = form.elements['priority'].value
    let destination_to_department = form.elements['destination_to_department'].value
    let destination_to_user = form.elements['destination_to_user'].value

    let data = {
        'title': title,
        'description': description,
        'type': type,
        'start_date': start_date,
        'done_at': done_at,
        'deadline': deadline,
        'status': status,
        'priority': priority,
        'destination_to_department': destination_to_department,
        'destination_to_user': destination_to_user
    }

    let token = localStorage.getItem('apiToken');
    let response = await makeRequest(form.action, "POST", data, token);

    await addTask(
        response.title,
        response.type,
        response.status,
        response.priority,
        response.deadline,
        response.author,
        `/task/${response.id}/`);


}


    async function addTask(title, type, status, priority, deadline, author, url) {
        let tableBody = document.getElementById('table_body')

        let newTask = document.createElement('tr');
        newTask.classList.add('detail-btn_task');
        newTask.dataset.detail_task = url;
        newTask.style.cursor = 'pointer'

        let taskTitle = document.createElement('td');
        taskTitle.textContent = title;

        let taskType = document.createElement('td');
        taskType.textContent = type;
        taskType.setAttribute('style', 'cursor: pointer');

        let taskStatus = document.createElement('td');
        taskStatus.textContent = status;

        let taskPriority = document.createElement('td');
        taskPriority.textContent = priority;

        let taskDeadline = document.createElement('td');
        taskDeadline.textContent = deadline;

        let taskAuthor = document.createElement('td');
        taskAuthor.textContent = author;

        newTask.appendChild(taskTitle);
        newTask.appendChild(taskType);
        newTask.appendChild(taskStatus);
        newTask.appendChild(taskPriority);
        newTask.appendChild(taskDeadline);
        newTask.appendChild(taskAuthor);

        tableBody.appendChild(newTask);
    }


async function onGetInfo(e) {
    e.preventDefault()
    let element = e.currentTarget
    console.log(element)
    let detail_attribute = element.data['detail_task']
    console.log(detail_attribute)
    let response = await makeRequest(detail_attribute, "GET")
    console.log(response)
}


function onLoad() {
    let action_buttons = document.getElementsByClassName('action-btn_task')
    console.log(action_buttons)
    for (let action_button of action_buttons) {
        action_button.addEventListener('click', onClick)
    }
    let detail_buttons = document.getElementsByClassName('detail-btn_task')
    for (let detail_button of detail_buttons) {
        detail_button.addEventListener('click', onGetInfo)
    }
}




window.addEventListener('load', onLoad);
// function onLoad(e) {
//     e.preventDefault();
//     let action_buttons = document.getElementsByClassName('action-btn_task')
//     console.log(action_buttons)
//     for (let action_button of action_buttons) {
//         action_button.addEventListener('click', onClick)
//     }
// }


// window.addEventListener('load', onLoad);

// function showModal(objectId) {
//     // 1. API
//     // 1.1 Get task JSON
//     // 1.2 Update task JSON
//     $('#modal-title').text(`Object id: ${objectId}`);
//     $('#taskModal').modal('show')
// }

// function showCreateModal() {
//     $('#taskCreateModal').modal('show')
// }

