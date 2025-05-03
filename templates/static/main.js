const radio_group = document.getElementById('radioGroup');
const search_input = document.getElementById('search');
const radios = radio_group.querySelectorAll('.radio-container');
 
const page_size = 5
const min_page = 1
let max_page = Math.ceil(radios.length / page_size)
let current_page = min_page

function filter_page() { 
    const query = search_input.value.toLowerCase();
    
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

    if (count_max > count) { count_max = count-1 }
    
    document.getElementById('page_label').innerHTML = `showing ${count_min + 1} - ${count_max} of ${count - 1}`

    if (current_page == max_page || count==1) {
        document.getElementById('next_svg').style.stroke = '#e0e0e0'
    } else { document.getElementById('next_svg').style.stroke = '#333' }

    if (current_page == 1 || count==1) {
        document.getElementById('prev_svg').style.stroke = '#e0e0e0'
    } else { document.getElementById('prev_svg').style.stroke = '#333' }

}

function open_modal(){
    document.getElementById('modal').style.display = 'block'
}

function close_modal(){
    document.getElementById('modal').style.display = 'none'
}

window.onclick = function(event) {
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
