console.log('Js work!')
var button = document.getElementById('button-order-create')
book_id = button.dataset.book_id
book_name = button.dataset.book_name

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
button.addEventListener('click', function (e) {
    e.preventDefault()
    button.innerHTML = ''
    console.log('Submit', book_id)
    url = '/library/api/order/create/'
    fetch(url, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken
        },
        // body: JSON.stringify({'book': book_id,'start_date': "2021-06-22T19:59:00Z", 'end_date': '2021-07-22T21:57:59Z'})
        body: JSON.stringify({'book': book_id})
    }).then(function (response) {
        alert('You rent the book ' + book_name + 'for 7 days')
        window.location.href = "/library/"
    })
})