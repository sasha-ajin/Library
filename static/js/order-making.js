console.log('Js work!')


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


const csrftoken = getCookie('csrftoken');
document.querySelectorAll('#button-order-create').forEach(button => {
    button.addEventListener('click', function (e) {
        const book_id = button.dataset.book_id;
        const book_name = button.dataset.book_name;
        const days_to_rent = document.getElementById('select-day-' + book_id).value;
        console.log(days_to_rent)
        button.innerHTML = ''
        console.log('Submit', book_id)
        url = '/library/api/order/create/'
        fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
            },
            body: JSON.stringify({'book': book_id, 'days_to_rent': days_to_rent})
        }).then(function (response) {
            alert('You rent the book ' + book_name + 'for ' + days_to_rent + ' days')
            window.location.href = "/library/"
        })
    })
})
