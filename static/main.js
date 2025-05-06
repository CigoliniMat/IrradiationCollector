const radio_group = document.getElementById('radioGroup');
const search_input = document.getElementById('search');
let radios = radio_group.querySelectorAll('.radio-container');
const add_form = document.getElementById('add_form')
const location_form = document.getElementById('location_form')
let api_running = false

const page_size = 5
const min_page = 1
let max_page = Math.ceil(radios.length / page_size)
let current_page = min_page

function create_list(location_list) {
    if (Array.isArray(location_list) == false) { alert(location_list) } else {
        radio_group.innerHTML = ''
        location_list.forEach(location => {
            const lbl = document.createElement('label')
            lbl.classList.add("radio-container")

            const input = document.createElement("input")
            input.type = "radio"
            input.name = "selection"
            input.value = location[0]

            const strong = document.createElement("strong")
            strong.textContent = location[1]

            const small = document.createElement("small")
            small.textContent = `[${location[2]} - ${location[3]}]`

            const description = document.createElement("small")
            description.textContent = location[4]

            lbl.appendChild(input)
            lbl.appendChild(strong)
            lbl.appendChild(small)
            lbl.appendChild(description)

            radio_group.appendChild(lbl)

        })
    }
}

function filter_page() {
    const query = search_input.value.toLowerCase();
    let radios = radio_group.querySelectorAll('.radio-container');

    let count = 1
    let count_min = 0
    let count_max = 0
    count_min = page_size * (current_page - 1)
    count_max = count_min + page_size
    radios.forEach(radio => {
        const label_text = radio.textContent.toLowerCase();
        if (label_text.includes(query)) {
            if (count > count_min && count <= count_max) {
                radio.classList.remove('hidden')
            } else { radio.classList.add('hidden') }; count++
        } else {
            radio.classList.add('hidden');
        }

        const chk_input = radio.querySelector('input');
        if (chk_input) {
            chk_input.checked = false;
        }
    });
    max_page = Math.ceil((count - 1) / page_size)

    if (count_max > count) { count_max = count - 1 }

    document.getElementById('page_label').innerHTML = `showing ${count_min + 1} - ${count_max} of ${count - 1}`

    if (current_page == max_page || count == 1) {
        document.getElementById('next_svg').style.stroke = '#e0e0e0'
    } else { document.getElementById('next_svg').style.stroke = '#333' }

    if (current_page == 1 || count == 1) {
        document.getElementById('prev_svg').style.stroke = '#e0e0e0'
    } else { document.getElementById('prev_svg').style.stroke = '#333' }

}

function open_modal() {
    document.getElementById('modal').style.display = 'block'
}

function close_modal() {
    document.getElementById('modal').style.display = 'none'
}

window.onclick = function (event) {
    const modale = document.getElementById('modal');
    if (event.target === modale) {
        close_modal();
    }
}

document.getElementById('next_btn').addEventListener('click', () => {
    if (current_page < max_page) {
        current_page++;
        filter_page();
    }
});

document.getElementById('prev_btn').addEventListener('click', () => {
    if (current_page > 1) {
        current_page--;
        filter_page();
    }
});

document.addEventListener('DOMContentLoaded', filter_page)
search_input.addEventListener('input', filter_page)

add_form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const form_data = new FormData(add_form)
    const response = await fetch(add_form.action, {
        method: 'POST',
        body: form_data

    });

    const result = await response.json()

    create_list(result)

    add_form.reset()
    filter_page()
    close_modal()
})

location_form.addEventListener('submit', async (event) => {
    event.preventDefault();

    const pressed_button = document.activeElement;
    const action = pressed_button.value
    const selected_location = new FormData(location_form)

    if (action == 'download_csv') {
        pressed_button.innerHTML = '<strong>downloading csv...</strong>';
        pressed_button.classList.add('working_btn');
        pressed_button.disabled = true;

        const response = await fetch('/download_csv', {
            method: 'POST',
            body: selected_location
        });

        if (response.ok) {
            const blob = await response.blob();
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement('a');
            a.style.display = 'none';
            a.href = url;
            const contentDisposition = response.headers.get('Content-Disposition');
            const fileName = contentDisposition ? contentDisposition.split('filename=')[1].replace(/"/g, '') : 'locations.csv';
            a.download = fileName;
            document.body.appendChild(a);
            a.click();
            window.URL.revokeObjectURL(url);
            document.body.removeChild(a);
        } else {
            console.error('Failed to download CSV');
        }

        pressed_button.classList.remove('working_btn');
        pressed_button.disabled = false;
        pressed_button.innerHTML = '<strong>Download CSV</strong>'
    
    } else if (action == 'update_api') {

        pressed_button.innerHTML = '<strong>Updating data...</strong>'
        pressed_button.classList.add('working_btn')
        pressed_button.disabled = true
        const response = await fetch('/update_api', {
            method: 'POST',
            body: selected_location
        })
        const result = await response.json()
        pressed_button.classList.remove('working_btn')
        pressed_button.disabled = false
        pressed_button.innerHTML = '<strong>Update location data</strong>'

    } else if (action == 'delete') {
        const sel = document.querySelector('input[name="selection"]:checked')
        if (sel) {
            const txt = sel.parentElement.querySelector('strong').textContent
            const conf = confirm(`delete location ${txt}?`);
            if (conf) {
                const response = await fetch('/delete_location', {
                    method: 'POST',
                    body: selected_location
                })
                const result = await response.json()

                create_list(result)

                location_form.reset()
                filter_page()
                close_modal()

            } else { console.debug("you don't select any location!") }
        }

    }

}

)
