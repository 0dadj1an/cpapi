function serverPost(url, payload, element) {
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
    serverPost(url, postData, element);
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

function onoffnat() {
    var check = document.getElementById("method");
    if (check.disabled == true) {
        document.getElementById("method").disabled = false;
        document.getElementById("gateway").disabled = false;
        document.getElementById("target").disabled = false;
    } else {
        document.getElementById("method").disabled = true;
        document.getElementById("gateway").disabled = true;
        document.getElementById("ipv4address").disabled = true;
        document.getElementById("target").disabled = true;
    }
}

function enableip() {
    document.getElementById("ipv4address").disabled = false;
}

function disableip() {
    document.getElementById("ipv4address").disabled = true;
}

function disablemethods() {
    var method = document.getElementById("method");
    if (method.value == "static") {
        document.getElementById("gateway").disabled = true;
        document.getElementById("ipaddress").disabled = true;
        enableip();
    } else {
        document.getElementById("gateway").checked = true;
        document.getElementById("gateway").disabled = false;
        document.getElementById("ipaddress").disabled = false;
        disableip();
    }
}

$(document).ready(function() {
    $('.selectjs').select2();
});
