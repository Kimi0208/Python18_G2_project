import {makeRequest, onLoad, onClick} from './main.js';


    async function onClick2(e){
        e.preventDefault()
        let element = e.currentTarget;
        let data_attribute= element.dataset['show_list']
        let response = await makeRequest(data_attribute, "GET")
        let datar = await response.text();
        let main_area = document.getElementById('main_area')
        main_area.innerHTML = datar
        onLoad()
        }



    function onLoad2() {
            let action_buttons = document.getElementsByClassName('show_list')
            for (let action_button of action_buttons) {
                action_button.addEventListener('click', onClick2)
            }
        }
    window.addEventListener('load', onLoad2);

