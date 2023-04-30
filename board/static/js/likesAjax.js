

var elements = document.getElementsByClassName("like-icon");

var toogleLike = function () {
    var meepNumber = this.getAttribute("id");
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
                this.setAttribute("stroke","#58A3EA");
                document.getElementById('likes/' + this.getAttribute('id'))
                .innerHTML=data['count']; //busco el contador que corresponde a este meep
                console.log(data['count'])
            } else {                                                 // el name del svg es = al id del meep que active 
                this.setAttribute("fill", "none");
                this.setAttribute("stroke","#707B7C");
                document.getElementById('likes/' + this.getAttribute('id'))
                .innerHTML=data['count']; //busco el contador que corresponde a este meep
                console.log(data['count'])
            }
        });
};

for (element of elements) {
    element.addEventListener("click", toogleLike);
    element.setAttribute("cursor","pointer")
}



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