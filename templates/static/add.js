const form = document.getElementById('adding_form')
form.addEventListener('submit', async (event) => {
    event.preventDefault(); // prevent default form submission

    const form_data = new FormData(form)
    const response = await fetch(form.action, {
        method: 'POST',
        body: form_data
    });

    const result = await response.json()

    alert(result['message']);
    window.location.href = '/'

})