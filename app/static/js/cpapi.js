function responsePost(url, payload, element) {
    var url = url;
    var method = "POST";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        element.innerText = data;
    }
    request.open(method, url);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(JSON.stringify(payload));
}

function customPost() {
    var url = window.location.href;
    var postData = {};
    var command = document.getElementById("command").value;
    var payload = document.getElementById("payload").value;
    var element = document.getElementById("json")
    postData["command"] = command;
    postData["payload"] = payload;
    responsePost(url, postData, element);
}

function commandPost() {
    console.log('hi');
    var url = window.location.href;
    var method = "POST";
    var postData = {};
    var targets = document.getElementById("targets").value;
    var script = document.getElementById("script").value;
    var element = document.getElementById("json");
    console.log(element);
    postData["targets"] = targets;
    postData["script"] = script;
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        console.log(data);
        console.log(element);
        element.innerText = data;
    }
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
