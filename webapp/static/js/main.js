async function makeRequest(url, method = 'GET', data = null, token = null) {
    let headers = {
    };
    if (token) {
        headers['Authorization'] = 'Token ' + token;

    }
    let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    headers['X-CSRFToken'] = csrftoken;
    let options;

    if (method !== "GET") {
        options = { method, headers, body: data };
    } else {
        options = { method, headers };
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
    let formData = new FormData(form);
    let token = localStorage.getItem('apiToken');
    let response = await makeRequest(form.action, "POST", formData, token);
    if (form.action.includes('create')) {
        console.log(response.id)
        await addTask(
        response.id,
        response.title,
        response.type,
        formatDate(response.created_at),
        response.status,
        response.priority,
        formatDate(response.deadline),
        response.author,
        `/task/${response.id}/`);
    } else if (form.action.includes('update')) {
        await updateTableTask(response.id, response.title, response.type, response.status, response.priority, formatDate(response.deadline));
        await updateDetailTaskInfo(response.id, response.title, response.type, response.status, response.priority,
            formatDate(response.deadline), formatDate(response.start_date), formatDate(response.updated_at), formatDate(response.done_at))

    }

}
async function updateTableTask(id, title, type, status, priority, deadline) {
    let task_title = document.getElementById(`task_${id}_title`)
    let task_type = document.getElementById(`task_${id}_type`)
    let task_status = document.getElementById(`task_${id}_status`)
    let task_priority = document.getElementById(`task_${id}_priority`)
    let task_deadline = document.getElementById(`task_${id}_deadline`)
    task_title.innerHTML = title
    task_type.innerHTML = type
    task_status.innerHTML = status
    task_priority.innerHTML = priority
    task_deadline.innerHTML = deadline

}

async function updateDetailTaskInfo(id, title, type, status, priority, deadline, start_date, updated_at, done_at){
    let detail_task_title = document.getElementsByClassName(`detail_task_${id}_title`)
    let detail_task_type = document.getElementsByClassName(`detail_task_${id}_type`)
    let detail_task_start_date = document.getElementsByClassName(`detail_task_${id}_start_date`)
    let detail_task_status = document.getElementsByClassName(`detail_task_${id}_status`)
    let detail_task_priority = document.getElementsByClassName(`detail_task_${id}_priority`)
    let detail_task_deadline = document.getElementsByClassName(`detail_task_${id}_deadline`)
    let detail_task_updated_at = document.getElementsByClassName(`detail_task_${id}_updated_at`)
    let detail_task_done_at = document.getElementsByClassName(`detail_task_${id}_done_at`)


    for (title_element of detail_task_title){
        title_element.innerHTML = `#${id} ${title}`
    }
    for (type_element of detail_task_type){
        type_element.innerHTML = `Тип: ${type}`
    }
    for (start_date_element of detail_task_start_date){
        start_date_element.innerHTML = `Начать: ${start_date}`
    }
    for (status_element of detail_task_status){
        status_element.innerHTML = `Статус: ${status}`
    }
    for (priority_element of detail_task_priority){
        priority_element.innerHTML = `Приоритет: ${priority}`
    }
    for (updated_at_element of detail_task_updated_at){
        updated_at_element.innerHTML = `Изменена: ${updated_at}`
    }
    for (done_at_element of detail_task_done_at){
        done_at_element.innerHTML = `Выполнена: ${done_at}`
    }
    for (deadline_element of detail_task_deadline){
        deadline_element.innerHTML = `Дедлайн: ${deadline}`
    }
}
async function addTask(id, title, type, created_at, status, priority, deadline, author, url) {
    let tableBody = document.getElementById('table_body')

    let newTask = document.createElement('tr');
    newTask.classList.add('detail-btn_task');
    newTask.dataset.detail_task = url;
    newTask.style.cursor = 'pointer'
    newTask.id=`task_id_${id}`
    newTask.addEventListener('click', onGetDetailTask)

    let taskTitle = document.createElement('td');
    taskTitle.textContent = title;
    taskTitle.id = `task_${id}_title`


    let taskType = document.createElement('td');
    taskType.textContent = type;
    taskType.id = `task_${id}_type`
    taskType.setAttribute('style', 'cursor: pointer');

    let taskStatus = document.createElement('td');
    taskStatus.textContent = status;
    taskStatus.id = `task_${id}_status`

    let taskPriority = document.createElement('td');
    taskPriority.textContent = priority;
    taskPriority.id = `task_${id}_priority`

    let taskCreatedAt = document.createElement('td');
    taskCreatedAt.textContent = created_at;
    taskCreatedAt.id = `task_${id}_created_at`

    let taskDeadline = document.createElement('td');
    taskDeadline.textContent = deadline;
    taskDeadline.id = `task_${id}_deadline`

    let taskAuthor = document.createElement('td');
    taskAuthor.textContent = author;
    taskAuthor.id = `task_${id}_author`

    newTask.appendChild(taskTitle);
    newTask.appendChild(taskType);
    newTask.appendChild(taskStatus);
    newTask.appendChild(taskPriority);
    newTask.appendChild(taskCreatedAt)
    newTask.appendChild(taskDeadline);
    newTask.appendChild(taskAuthor);

    tableBody.appendChild(newTask);
}

function formatDate(dateTimeString) {
    if (!dateTimeString) return '';
    const dateTime = new Date(dateTimeString);
    const year = dateTime.getFullYear();
    const month = ('0' + (dateTime.getMonth() + 1)).slice(-2);
    const day = ('0' + dateTime.getDate()).slice(-2);
    const hours = ('0' + dateTime.getHours()).slice(-2);
    const minutes = ('0' + dateTime.getMinutes()).slice(-2);
    return `${day}-${month}-${year} ${hours}:${minutes}`;
}


async function onGetDetailTask(e) {
    e.preventDefault()
    let element = e.currentTarget
    let detail_attribute = element.dataset['detail_task']
    let task_detail_info_element = document.getElementById('task-detail-info')
    task_detail_info_element.style.display = 'block'
    let response = await makeRequest(detail_attribute, "GET")
    let response_data = response.task

    let task_edit = document.getElementById('task_edit')
    task_edit.dataset.action_task = `update/${response_data.id}/`

    let task_add_file = document.getElementById('add_file')
    task_add_file.dataset.action_task = `task/${response_data.id}/file/add/`

    let task_files = document.getElementById('task_files')
    task_files.dataset.get_info_task = `task/${response_data.id}/files/`

    let create_subtask = document.getElementById('add_subtask')
    create_subtask.dataset.action_task = `task/${response_data.id}/create_subtask/`

    let task_title = document.getElementById('task_title')
    task_title.innerHTML = `#${response_data.id} ${response_data.title}`
    task_title.classList.add(`detail_task_${response_data.id}_title`)

    let task_created_at = document.getElementById('task_created_at')
    task_created_at.innerHTML = `Создана: ${formatDate(response_data.created_at)}`

    let task_start_date = document.getElementById('task_start_date')
    task_start_date.innerHTML = `Начать: ${formatDate(response_data.start_date)}`
    task_start_date.classList.add(`detail_task_${response_data.id}_start_date`)

    let task_status = document.getElementById('task_status')
    task_status.innerHTML = `Статус: ${response_data.status}`
    task_status.classList.add(`detail_task_${response_data.id}_status`)

    let task_priority = document.getElementById('task_priority')
    task_priority.innerHTML = `Приоритет: ${response_data.priority}`
    task_priority.classList.add(`detail_task_${response_data.id}_priority`)

    let task_updated_at = document.getElementById('task_updated_at')
    task_updated_at.innerHTML = `Изменена: ${formatDate(response_data.updated_at)}`
    task_updated_at.classList.add(`detail_task_${response_data.id}_updated_at`)

    let task_done_at = document.getElementById('task_done_at')
    task_done_at.innerHTML = `Выполнена: ${formatDate(response_data.done_at)}`
    task_done_at.classList.add(`detail_task_${response_data.id}_done_at`)

    let task_deadline = document.getElementById('task_deadline')
    task_deadline.innerHTML = `Дедлайн: ${formatDate(response_data.deadline)}`
    task_deadline.classList.add(`detail_task_${response_data.id}_deadline`)

    let task_author = document.getElementById('task_author')
    task_author.innerHTML = `От кого: ${response_data.author}`

    let task_type = document.getElementById('task_type')
    task_type.innerHTML = `Тип: ${response_data.type}`
    task_type.classList.add(`detail_task_${response_data.id}_type`)

}

async function onGetInfo(e) {
    e.preventDefault();
    let element = e.currentTarget;
    let data_attribute = element.dataset['get_info_task'];
    let response = await makeRequest(data_attribute, "GET");
    let modal = document.getElementById('action-task-modal_window');
    modal.style.display = 'block';
    modal.innerHTML = '';
    let files = response.files
    modal.innerHTML = `
            <div class="modal-content action_task_modal-content">
                <div>
                    <div class="form-modal-header action_task_form-modal-header">
                        <h4>Файлы </h4>
                        <button id="close_modal" style="background: white; border: none">Закрыть</button>
                    </div>
                    <div class="card" style="width: 18rem;">
                        <ul class="list-group list-group-flush">
                                
                        </ul>
                    </div>
                </div>
            </div>
    `
    let ul_element = document.getElementsByClassName('list-group-flush')[0]
    files.forEach(file => {
        ul_element.innerHTML += `
           <li class="list-group-item" id="file_${file.id}">
                <p>${file.name.replace("uploads/user_docs/", "")}</p>
                <a href="${file.url}" target="_blank" download="">Скачать</a>
                <a href="task/${file.task_id}/file/${file.id}/delete/" class="file_delete">Удалить</a><br>
                
                <div class="confirmation_file_delete" id="confirmation_file-${file.id}_delete" style="display: none; margin-top: 5px"></div>
           </li>`;
    });
    let closeBtn = document.getElementById("close_modal");
    closeBtn.onclick = function () {
        modal.style.display = "none";
        modal.innerHTML = ''
    }
    let file_delete_buttons = document.getElementsByClassName('file_delete')
    for (let file_delete_button of file_delete_buttons) {
        file_delete_button.addEventListener('click', onConfirmDeletion)
    }

}

async function onConfirmDeletion(e){
    e.preventDefault()
    let element = e.currentTarget
    let data_attribute = element.getAttribute('href')
    let response = await makeRequest(data_attribute, "GET")
    let data = await response.text()
    let listItem = element.closest('li'); // Найти родительский элемент списка
    let fileId = listItem.id.split('_')[1]; // Получить идентификатор файла из атрибута id
    let confirmation_file_delete_elements = document.getElementsByClassName('confirmation_file_delete')
    for (confirmation_file_delete_element of confirmation_file_delete_elements){
        if (confirmation_file_delete_element.style.display = 'block') {
                confirmation_file_delete_element.style.display = 'none'
                confirmation_file_delete_element.innerHTML=''
        }
    }
    let div_element = document.getElementById(`confirmation_file-${fileId}_delete`)
    div_element.innerHTML = data
    div_element.style.display='block'
    let confirm_delete_button = document.getElementById('confirm_delete')
    let cancel_delete_button = document.getElementById('cancel_delete')
    confirm_delete_button.addEventListener('click', async function(){
        let post_response = await makeRequest(data_attribute, "POST")
        listItem.remove()
    })
    cancel_delete_button.addEventListener('click', async function(){
        div_element.innerHTML = ''
        div_element.style.display='none'
    })

}


function onLoad() {
    let action_buttons = document.getElementsByClassName('action-btn_task')
    for (let action_button of action_buttons) {
        console.log(action_button)
        action_button.addEventListener('click', onClick)
    }
    let detail_buttons = document.getElementsByClassName('detail-btn_task')
    for (let detail_button of detail_buttons) {
        detail_button.addEventListener('click', onGetDetailTask)
    }
    let get_info_buttons = document.getElementsByClassName('get-info-btn_task')
    for (let get_info_button of get_info_buttons) {
        get_info_button.addEventListener('click', onGetInfo)
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

