




function getCookie(name)
{
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') 
    {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) 
        {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '='))
            {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
const csrftoken = getCookie('csrftoken');

$(".form-check-input").on('change', function (ev)
{
    const $this = $(this);
    const request = new Request(
        'http://127.0.0.1:8000/correct/',
        {
            headers:{
                'X-CSRFToken': csrftoken,
                'Content-type' : 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            method: 'POST',
            body: 'answer_id=' + $this.data('id'),
        }
    );
    fetch(request).then(function(response)
    {
        response.json().then(function(parsed)
        {
            
        });
    });
});

$(".love-btn").on('click', function (ev)
{
    const $this = $(this);
    const request = new Request(
        'http://127.0.0.1:8000/vote_up/',
        {
            headers:{
                'X-CSRFToken': csrftoken,
                'Content-type' : 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            method: 'POST',
            body: 'question_id=' + $this.data('id'),
        }
    );
    fetch(request).then(function(response)
    {
        response.json().then(function(parsed)
        {
            $this.text(parsed.new_rating + " Likes");
        });
    });
});



$(".love-btn-answer").on('click', function (ev)
{
    const $this = $(this);
    const request = new Request(
        'http://127.0.0.1:8000/vote_up_for_answer/',
        {
            headers:{
                'X-CSRFToken': csrftoken,
                'Content-type' : 'application/x-www-form-urlencoded;charset=UTF-8'
            },
            method: 'POST',
            body: 'answer_id=' + $this.data('id'),
        }
    );
    fetch(request).then(function(response)
    {
        response.json().then(function(parsed)
        {
            $this.text(parsed.new_rating + " Likes");
        });
    });
});
