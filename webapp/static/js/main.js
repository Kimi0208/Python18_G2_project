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
    showLoadingProcess()
    e.preventDefault();
    let form = e.target.closest('form');
    let formData = new FormData(form);
    let token = localStorage.getItem('apiToken');
    let response = await makeRequest(form.action, "POST", formData, token);
    let modal = document.getElementById('action-task-modal_window');
    if ('errors' in response){
        for (let error of response.errors.__all__) {
            alert(error)
        }
    } else {
        if (form.action.includes('create_subtask')) {
            let task_subtasks = response.subtasks
            let subtasks_info = document.getElementById('subtasks_info')
            if (task_subtasks.length > 0) {
                subtasks_info.innerHTML = '';
                await createTaskTable(task_subtasks, subtasks_info);
            } else {
                subtasks_info.innerHTML = 'Подзадач нет';
            }
        }
        if (form.action.includes('/task/create/') || form.action.includes('create_subtask')) {
            let tableBody = document.getElementById('table_body')
            let whose_table = tableBody.dataset['whose_table']
            if (whose_table === response.destination_to) {
                await addTask(
                response.id,
                response.title,
                response.type,
                formatDate(response.created_at),
                response.status,
                response.priority,
                formatDate(response.deadline),
                response.author,
                response.destination_to,
                `/task/${response.id}/`);
            }
            modal.style.display = 'none'
            modal.innerHTML = ''
        } else if (form.action.includes('task') && form.action.includes('update')) {
            await updateTableTask(response.id, response.title, response.type, response.status, response.priority,
                formatDate(response.deadline), response.destination_to);

            await updateDetailTaskInfo(response.id, response.title, response.type, response.status, response.priority,
                formatDate(response.deadline), formatDate(response.start_date), formatDate(response.updated_at),
                formatDate(response.done_at), response.description)

        } else if (form.action.includes('comment/create/')) {
            let comment = response.comment
            await addComment(comment.id, comment.author_first_name, comment.author_last_name, comment.task,
                comment.created_at, comment.updated_at, comment.description, comment.author_id, comment.user_id)
        } else if (form.action.includes('comment') && form.action.includes('update')){
            let comment = response.comment
            await editComment(comment.id, comment.author_first_name, comment.author_last_name, comment.task,
                comment.created_at, comment.updated_at, comment.description, comment.author_id, comment.user_id)
        } else if (form.action.includes('file/add/')){
            modal.style.display = 'none'
            modal.innerHTML = ''
        }

    }
    hideLoadingProcess()
}

async function editComment(id, first_name, last_name, task, created_at, updated_at, description, author_id, user_id) {
    let comment_data = document.getElementById(`comment_data_${id}`)
    comment_data.innerHTML = description
    let modal = document.getElementById('action-task-modal_window');
    modal.style.display = 'none'
    modal.innerHTML = ''
}


async function addComment(id, first_name, last_name, task, created_at, updated_at, description, author_id, user_id){
    let comments_info_block = document.getElementById('comments_info')
    let comment_card = document.createElement('div')
    comment_card.style.borderBottom = 'solid 1px black'
    comment_card.style.marginBottom = '10px'
    comment_card.id = `comment_card_${id}`
    if (user_id === author_id) {
        let action_comment_block = document.createElement('div')
        action_comment_block.style.display = 'flex'
        action_comment_block.style.justifyContent = 'flex-end'
        let edit_comment_button = document.createElement('button')
        edit_comment_button.type = 'button'
        edit_comment_button.style.border = 'none'
        edit_comment_button.style.padding = '0px'
        edit_comment_button.style.background = 'none'
        let edit_comment_icon = document.createElement('i')
        edit_comment_icon.classList.add('fas', 'fa-fw', 'fa-edit')
        edit_comment_button.dataset.action_task = `comment/${id}/update/`
        edit_comment_button.addEventListener('click', onClick)
        edit_comment_button.appendChild(edit_comment_icon)

        let delete_comment_button = document.createElement('button')
        delete_comment_button.type = 'button'
        delete_comment_button.style.border = 'none'
        delete_comment_button.style.padding = '0px'
        delete_comment_button.style.background = 'none'
        let delete_comment_icon = document.createElement('i')
        delete_comment_icon.classList.add('fas', 'fa-fw', 'fa-trash-alt')
        delete_comment_button.dataset.delete_comment = `comment/${id}/delete/`
        delete_comment_button.dataset.comment_id = `${id}`
        delete_comment_button.addEventListener('click', onSubmitCommentDelete)
        delete_comment_button.appendChild(delete_comment_icon)

        let confirm_comment_delete_field = document.createElement('div')
        confirm_comment_delete_field.classList.add('confirmation_comment_delete')
        confirm_comment_delete_field.id = `confirmation_comment_${id}_delete`
        confirm_comment_delete_field.style.display = 'none'

        action_comment_block.appendChild(edit_comment_button)
        action_comment_block.appendChild(delete_comment_button)
        comment_card.appendChild(action_comment_block)
        comment_card.appendChild(confirm_comment_delete_field)

    }
    let comment_card_body = document.createElement('div')

    let username_info = document.createElement('span')
    username_info.innerHTML = `${first_name} ${last_name}`
    username_info.style.fontStyle='italic'
    username_info.style.fontWeight='bold'
    let create_info = document.createElement('p')
    create_info.innerHTML = formatDate(created_at)
    create_info.style.fontWeight='bold'
    let comment_info = document.createElement('span')
    comment_info.innerHTML = description
    comment_info.id = `comment_data_${id}`
    let comment_header = document.createElement('div')
    comment_header.style.display = 'flex'
    comment_header.style.justifyContent = 'space-between'
    comment_card_body.appendChild(comment_info)

    comment_header.appendChild(username_info)
    comment_header.appendChild(create_info)

    comment_card.appendChild(comment_header)
    comment_card.appendChild(comment_card_body)
    if (comments_info_block.innerHTML === 'Комментариев нет') {
        comments_info_block.innerHTML = ''
    }
    let firstComment = comments_info_block.firstChild;

    if (firstComment) {
        comments_info_block.insertBefore(comment_card, firstComment);
    } else {
        comments_info_block.appendChild(comment_card);
    }
    let modal = document.getElementById('action-task-modal_window');
    modal.style.display = 'none'
    modal.innerHTML = ''

}


async function onSubmitCommentDelete(e) {
    showLoadingProcess
    e.preventDefault()
    let element = e.currentTarget
    let data_attribute = element.dataset['delete_comment']
    let response = await makeRequest(data_attribute, "GET")
    let data = await response.text()
    let comment_id = element.dataset['comment_id']

    let confirmation_comment_delete_elements = document.getElementsByClassName('confirmation_comment_delete')
    for (confirmation_comment_delete_element of confirmation_comment_delete_elements) {
        if (confirmation_comment_delete_element.style.display === 'block') {
            confirmation_comment_delete_element.style.display = 'none'
            confirmation_comment_delete_element.innerHTML = ''
        }
    }
    let confirmation_comment_delete_field = document.getElementById(`confirmation_comment_${comment_id}_delete`)
    confirmation_comment_delete_field.innerHTML = data
    confirmation_comment_delete_field.style.display = 'block'
    confirmation_comment_delete_field.style.marginBottom = '10px'
    let confirm_delete_button = document.getElementById('confirm_delete')
    let cancel_delete_button = document.getElementById('cancel_delete')
    confirm_delete_button.addEventListener('click', async function() {
        let post_response = await makeRequest(data_attribute, "POST")
        let comment_card = document.getElementById(`comment_card_${post_response.comment_id}`)
        comment_card.remove()
        let comments_info_field = document.getElementById('comments_info')
        if (comments_info_field.innerHTML === '') {
            comments_info_field.innerHTML = 'Комментариев нет'
        }
    })
    cancel_delete_button.addEventListener('click', async function() {
        confirmation_comment_delete_field.innerHTML = ''
        confirmation_comment_delete_field.style.display = 'none'
    })

    hideLoadingProcess()
}

async function updateTableTask(id, title, type, status, priority, deadline, destination_to) {
    let task = dataTable.row(`#task_id_${id}`)
    let tableBody = document.getElementById('table_body')
    let whose_table = tableBody.dataset['whose_table']

    if (whose_table === destination_to) {
        let data = [
            title,
            type,
            status,
            priority,
            task.data()[4],
            deadline,
            task.data()[6]
        ];
        task.data(data).draw()
        dataTable.columns.adjust().draw()

    } else if (whose_table !== destination_to) {
        task.remove().draw()
    }

}

async function updateDetailTaskInfo(id, title, type, status, priority, deadline, start_date, updated_at, done_at, description){
    let detail_task_title = document.getElementsByClassName(`detail_task_${id}_title`)
    let detail_task_type = document.getElementsByClassName(`detail_task_${id}_type`)
    let detail_task_start_date = document.getElementsByClassName(`detail_task_${id}_start_date`)
    let detail_task_status = document.getElementsByClassName(`detail_task_${id}_status`)
    let detail_task_priority = document.getElementsByClassName(`detail_task_${id}_priority`)
    let detail_task_deadline = document.getElementsByClassName(`detail_task_${id}_deadline`)
    let detail_task_updated_at = document.getElementsByClassName(`detail_task_${id}_updated_at`)
    let detail_task_done_at = document.getElementsByClassName(`detail_task_${id}_done_at`)
    let detail_task_description = document.getElementsByClassName(`detail_task_${id}_description`)


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
    for (description_element of detail_task_description){
        description_element.innerHTML = description
    }
    let modal = document.getElementById('action-task-modal_window');
    modal.style.display = 'none'
    modal.innerHTML = ''
}


async function onGetTasks(e) {
    showLoadingProcess()
    e.preventDefault()
    let element = e.currentTarget
    let get_tasks_buttons = document.getElementsByClassName('get-tasks_btn')
    for (let button of get_tasks_buttons) {
        if (button.style.background === 'lightgrey') {
            button.style.background = ''
        }
    }
    element.style.background = 'lightgrey'
    let data_attribute = element.dataset['get_tasks']
    let response = await makeRequest(data_attribute, "GET")
    let whose_table = element.dataset['whose_table']
    let tasks = response.tasks
    let tableBody = document.getElementById('table_body')
    tableBody.dataset.whose_table = whose_table
    dataTable.clear()
    for (let task of tasks) {
        let url = `/task/${task.id}/`
        await addTask(task.id, task.title, task.type, formatDate(task.created_at), task.status, task.priority, formatDate(task.deadline), task.author, task.destination_to, url)
    }
    dataTable.draw()
    hideLoadingProcess()
}


async function addTask(id, title, type, created_at, status, priority, deadline, author, destination_to, url) {
    let data = [
        title,
        type,
        status,
        priority,
        created_at,
        deadline,
        author
    ];
    let newTask = dataTable.row.add(data).draw().node();
    newTask.classList.add('detail-btn_task');
    newTask.dataset.detail_task = url;
    newTask.style.cursor = 'pointer';
    newTask.id = `task_id_${id}`;
    newTask.addEventListener('click', onGetDetailTask)

    let modal = document.getElementById('action-task-modal_window');
    modal.style.display = 'none'
    modal.innerHTML = ''
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

async function onAddChecklist(e) {
    showLoadingProcess()
    e.preventDefault()
    let element = e.currentTarget
    let data_attribute = element.dataset['add_checklist']
    let response = await makeRequest(data_attribute, "GET")
    let subtasks = response.subtasks
    let subtasks_info = document.getElementById('subtasks_info')
    subtasks_info.innerHTML = ''
    await createTaskTable(subtasks, subtasks_info)
    hideLoadingProcess()
}


async function onGetDetailTask(e) {
    showLoadingProcess()
    e.preventDefault();
    let element = e.currentTarget;
    let detail_attribute = element.dataset['detail_task'];
    let detail_tasks_buttons = document.getElementsByClassName('detail-btn_task')
    for (let button of detail_tasks_buttons) {
        if (button.style.background === 'lightgrey') {
            button.style.background = ''
        }
    }
    element.style.background = 'lightgrey'
    let task_detail_info_element = document.getElementById('task-detail-info');
    task_detail_info_element.style.display = 'block';
    let response = await makeRequest(detail_attribute, "GET");
    let response_data = response.task;

    let task_edit = document.getElementById('task_edit')
    task_edit.dataset.action_task = `task/${response_data.id}/update/`

    let task_add_file = document.getElementById('add_file')
    task_add_file.dataset.action_task = `task/${response_data.id}/file/add/`

    let task_files = document.getElementById('task_files')
    task_files.dataset.get_info_task = `task/${response_data.id}/files/`

    let create_subtask = document.getElementById('add_subtask')
    create_subtask.dataset.action_task = `task/${response_data.id}/create_subtask/`

    let task_history = document.getElementById('task_history')
    task_history.dataset.get_history_task = `task/${response_data.id}/history/`

    let comment_create = document.getElementById('comment_add')
    comment_create.dataset.action_task = `task/${response_data.id}/comment/create/`

    let add_checklist_btns = document.getElementsByClassName('add_checklist_btn')
    for (let add_checklist_btn of add_checklist_btns) {
        let checklist_id = add_checklist_btn.dataset['checklist_id']
        add_checklist_btn.dataset.add_checklist = `task/${response_data.id}/${checklist_id}/`
        add_checklist_btn.addEventListener('click', onAddChecklist)
    }

    task_history.addEventListener('click', onGetTaskHistory)

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

    let task_description = document.getElementById('task_description')
    task_description.innerHTML = response_data.description
    task_description.classList.add(`detail_task_${response_data.id}_description`)

    let task_subtasks = response_data.subtasks
    let subtasks_info = document.getElementById('subtasks_info')

    let parent_info_element = document.getElementById('parent_info')

    let comments_info = document.getElementById('comments_info')

    if (response_data.parent_task) {
        create_subtask.style.display = 'none'
        parent_info_element.innerHTML = '';
        await createTaskTable([response_data.parent_task], parent_info_element);
    } else {
        parent_info_element.innerHTML = 'Вышестоящих задач нет';
        create_subtask.style.display = 'block'
    }

    if (task_subtasks.length > 0) {
    subtasks_info.innerHTML = '';
    await createTaskTable(task_subtasks, subtasks_info);
    } else {
        subtasks_info.innerHTML = 'Подзадач нет';
    }

    if (response_data.comments.length > 0) {
        comments_info.innerHTML = ''
        let comments = response_data.comments
        for (let comment of comments) {
            await addComment(comment.id, comment.author_first_name, comment.author_last_name, comment.task, comment.created_at,
                comment.updated_at, comment.description, comment.author_id, comment.user_id)
        }
    } else {
        comments_info.innerHTML = 'Комментариев нет'
    }
    hideLoadingProcess()

}


async function onGetTaskHistory(e){
    showLoadingProcess()
    e.preventDefault()
    let element = e.currentTarget
    let data_atribute = element.dataset['get_history_task']
    let response = await makeRequest(data_atribute, "GET")
    let history = response.history
    let modal = document.getElementById('action-task-modal_window');
    modal.style.display = 'block';
    let modal_content = document.createElement('div')
    modal_content.classList.add('modal-content', 'action_task_modal-content')
    let div_header = document.createElement('div')
    div_header.classList.add('form-modal-header', 'action_task_form-modal-header')
    let h4_header = document.createElement('h4')
    h4_header.innerHTML = 'История'
    let closeBtn = document.createElement('button')
    closeBtn.id = 'close_modal'
    closeBtn.style.background = 'white'
    closeBtn.style.border = 'none'
    closeBtn.innerHTML = 'Закрыть'
    div_header.appendChild(h4_header)
    div_header.appendChild(closeBtn)
    modal_content.appendChild(div_header)
    modal.appendChild(modal_content)

    let card_element = document.createElement('div')
    card_element.classList.add('card')
    for (let changes of history){
        let ul_element = document.createElement('ul')
        let li_element = document.createElement('li')
        for (let change of changes) {

            if (change[0].includes('файл')){
                li_element.innerHTML = `${change[0]} ${change[3].replace("uploads/user_docs/", "")} 
                    <br>Дата: ${change[1]} Автор: ${change[2]}`
            } else if (change[0].includes('Создана задача') || change[0].includes('Создана подзадача')){
                li_element.innerHTML = `${change[0]} ${change[3]} <br>Дата создания: ${change[1]} Автор: ${change[2]}`
            } else if (change[0].includes('Изменен комментарий')) {
                li_element.innerHTML = `${change[0]} <br>Дата создания: ${change[1]} Автор: ${change[2]}`
            } else if (change[0].includes('Добавлен комментарий')) {
                li_element.innerHTML = `${change[0]} <br>Дата создания: ${change[1]} Автор: ${change[2]}`
            } else if (change[0].includes('Удален комментарий')) {
                li_element.innerHTML = `${change[0]} <br>Дата удаления: ${change[1]} Автор: ${change[2]}`
            } else {
                li_element.innerHTML += `Поле ${change[0]} изменено с ${change[3]} на ${change[4]} 
                    <br>Дата изменения: ${change[1]} Кто изменил: ${change[2]}<br>`
            }

        }
        ul_element.appendChild(li_element)
        card_element.appendChild(ul_element)
    }
    modal_content.appendChild(card_element)

    closeBtn.onclick = function () {
        modal.style.display = "none";
        modal.innerHTML = ''
    }
    hideLoadingProcess()
}

async function createTaskTable(taskData, infoElement) {
    if (!taskData || !infoElement) {
        return;
    }


    let table = document.createElement('table');
    table.style.width = '100%';
    table.id='subtask_table'

    let tr1 = document.createElement('tr');
    let nameTh = document.createElement('th');
    nameTh.innerHTML = 'Имя';
    nameTh.style.width = '60%'

    let typeTh = document.createElement('th');
    typeTh.innerHTML = 'Тип';

    let updateTh = document.createElement('th');
    updateTh.innerHTML = 'Изменена в';
    tr1.appendChild(nameTh);
    tr1.appendChild(typeTh);
    tr1.appendChild(updateTh);
    table.appendChild(tr1);

    taskData.forEach(task => {
        let tr = document.createElement('tr');
        let nameTd = document.createElement('td');
        let taskLink = document.createElement('a');
        if (task.status === "Выполнена"){
            taskLink.style.textDecoration='line-through'
        }
        taskLink.href = `task/${task.id}/`;
        taskLink.dataset.detail_task = taskLink.href;
        taskLink.innerHTML = `#${task.id} ${task.title} <br>От: ${task.author}<br> Кому: ${task.destination_to}`;
        taskLink.addEventListener('click', onGetDetailTask);

        nameTd.appendChild(taskLink);

        let typeTd = document.createElement('td');
        typeTd.innerHTML = task.type;

        let updateTd = document.createElement('td');
        updateTd.innerHTML = formatDate(task.updated_at);

        tr.appendChild(nameTd);
        tr.appendChild(typeTd);
        tr.appendChild(updateTd);

        table.appendChild(tr);
    });

    infoElement.appendChild(table);
}



async function onGetInfo(e) {
    showLoadingProcess()
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
                    <div style="width: 18rem;">
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
                <div id="action_field_file_${file.id}" style="display:flex; align-items: center;">
                    <a href="${file.url}" target="_blank" download="">Скачать</a>
                    <a href="task/${file.task_id}/file/${file.id}/delete/" class="file_delete">Удалить</a>
                </div>
                
                <div class="confirmation_file_delete" id="confirmation_file-${file.id}_delete" style="display: none; margin-top: 5px"></div>
           </li>`;
        let action_field = document.getElementById(`action_field_file_${file.id}`)
        if (file.sign_url) {
            if (response.signed_files.includes(file.id)) {
                action_field.innerHTML += `<span>Подписан</span>`
            } else {
                action_field.innerHTML += `
                    <div class="btn-group">
                      <button type="button" class="btn btn-link dropdown-toggle p-0" data-toggle="dropdown" aria-expanded="false">
                        Подпись
                      </button>
                      <div class="dropdown-menu">
                        <a class="dropdown-item sign_file" href="${file.sign_url}">Подписать файл</a>
                      </div>
                    </div>`
            }
        }
    });

    let closeBtn = document.getElementById("close_modal");
    closeBtn.onclick = function () {
        modal.style.display = "none";
        modal.innerHTML = ''
    }
    let sign_file_btns = document.getElementsByClassName('sign_file')
    for (let sign_file_btn of sign_file_btns) {
        sign_file_btn.addEventListener('click', onAddSign)
    }

    let file_delete_buttons = document.getElementsByClassName('file_delete')
    for (let file_delete_button of file_delete_buttons) {
        file_delete_button.addEventListener('click', onConfirmDeletion)
    }
    hideLoadingProcess()
}

async  function onAddSign(e){
    showLoadingProcess()
    e.preventDefault()
    let element = e.currentTarget
    let href_attribute = element.href
    let response = await makeRequest(href_attribute, "GET")
    if (response.success) {
        let spanElement = document.createElement('span');
        spanElement.innerHTML='Подписан'
        let parent_div = element.parentNode.parentNode
        parent_div.parentNode.replaceChild(spanElement, parent_div);

    }
    hideLoadingProcess()
}

async function onConfirmDeletion(e){
    showLoadingProcess()
    e.preventDefault()
    let element = e.currentTarget
    let data_attribute = element.getAttribute('href')
    let response = await makeRequest(data_attribute, "GET")
    let data = await response.text()
    let listItem = element.closest('li');
    let fileId = listItem.id.split('_')[1];
    let confirmation_file_delete_elements = document.getElementsByClassName('confirmation_file_delete')
    for (confirmation_file_delete_element of confirmation_file_delete_elements){
        if (confirmation_file_delete_element.style.display === 'block') {
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
        listItem.remove();
    })
    cancel_delete_button.addEventListener('click', async function(){
        div_element.innerHTML = ''
        div_element.style.display='none'
    })
    hideLoadingProcess()

}

async function onGetNewTask(){
    let blink_notification = document.getElementById('blink_notification');
    let response = await makeRequest('new_tasks/', "GET")
    if (response.task_count > 0) {
        blink_notification.style.display = 'block'
    } else {
        blink_notification.style.display = 'none'
    }
}

let dataTable;
function onLoad() {
    setInterval(async function() {
        await onGetNewTask() }, 5000);

    $(document).ready(function() {
          dataTable = $('#DataTable').DataTable();
    });

    let action_buttons = document.getElementsByClassName('action-btn_task')
    for (let action_button of action_buttons) {
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
    let get_tasks_buttons = document.getElementsByClassName('get-tasks_btn')
    for (let get_tasks_button of get_tasks_buttons) {
        get_tasks_button.addEventListener('click', onGetTasks)
    }
}


function showLoadingProcess() {
    console.log(123)
    let loader = document.getElementById('overlay')
    loader.style.display='flex'
}

function hideLoadingProcess() {
    let loader = document.getElementById('overlay')
    loader.style.display='none'
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