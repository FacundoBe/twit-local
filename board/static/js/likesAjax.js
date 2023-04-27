

var elements = document.getElementsByClassName("like-icon");

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

var toogleLike = function () {
    var meepNumber = this.getAttribute("name");
    fetch(window.location.href, {
        method: "POST",
        credentials: "same-origin",
        headers: {
            "X-Requested-With": "XMLHttpRequest",
            "X-CSRFToken": getCookie("csrftoken"),
        },
        body: JSON.stringify({ 'meepNumber': meepNumber })
    })
        .then(response => response.json())
        .then(data => {
            if (data['status'] === 'Like') {
                this.setAttribute("fill", "#58A3EA");
                document.getElementById('likes/' + this.getAttribute('name'))
                .innerHTML=data['count']; //busco el contador que corresponde a este meep
                console.log(data['count'])
            } else {                                                 // el name del svg es = al id del meep que active 
                this.setAttribute("fill", "none");
                document.getElementById('likes/' + this.getAttribute('name'))
                .innerHTML=data['count']; //busco el contador que corresponde a este meep
                console.log(data['count'])
            }
        });
};

for (var i = 0; i < elements.length; i++) {
    elements[i].addEventListener('click', toogleLike, false);

}
