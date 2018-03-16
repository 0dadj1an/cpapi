setInterval(function() {
    var local = document.getElementById("local");
    var remote = document.getElementById("remote");
    var url = window.location + "/objectcheck";
    var method = "GET";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        var resp = JSON.parse(data);
        local.innerText = resp.local;
        remote.innerText = resp.remote;
    }
    request.open(method, url);
    request.send();
}, 10000);
