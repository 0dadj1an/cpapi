function sandboxPost() {
    var url = window.location.href;
    var method = "POST";
    var postData = {};
    var command = document.getElementById("command").value;
    var payload = document.getElementById("payload").value;
    var element = document.getElementById("sandboxresponse");
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        var header = document.createElement("h1");
        var headerinfo = document.createTextNode("Response");
        var response = document.createElement("pre");
        var responsedata = document.createTextNode(data);
        header.appendChild(headerinfo);
        response.appendChild(responsedata);
        element.appendChild(header);
        element.appendChild(response);
    }
    postData["command"] = command;
    postData["payload"] = payload;
    request.open(method, url);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(JSON.stringify(postData));
}

function rulesearch() {
    var string = document.getElementById("searchstring").value;
    var table = document.getElementById("tbody");
    for (var i = 0, row; row = table.rows[i]; i++) {
        for (var j = 0, col; col = row.cells[j]; j++) {
            data = col.innerText;
            if (data.includes(string)) {
                row.removeAttribute("style");
                break;
            } else {
                row.style.display = "none";
            }
        }
    }
}

$(document).ready(function() {
    $('.selectjs').select2();
});
