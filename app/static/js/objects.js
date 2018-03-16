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
        if (resp.local != 0) {
            if (resp.local != resp.remote) {
                deltasync();
            }
        } else {
            fullsync();
        }
    }
    request.open(method, url);
    request.send();
}, 10000);

function deltasync() {
    console.log('deltasync');
}

function fullsync() {
    var url = window.location + "/fullsync";
    var method = "GET";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        showobjects();
    }
    request.open(method, url);
    request.send();
}

function showobjects() {
    showhosts();
    shownetworks();
}

function showhosts() {
    var container = document.getElementById("hostcontainer");
    var url = window.location + "/showhosts";
    var method = "GET";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        var resp = JSON.parse(data);
        var i = 0;
        var obj = 'hostname'
        for (i = 0, obj; obj = resp.objects[i]; i++) {
            var p = document.createElement("p");
            var info = document.createTextNode(obj);
            p.appendChild(info);
            container.appendChild(p);
        }
    }
    request.open(method, url);
    request.send();
}

function togglehost() {
    var container = document.getElementById("hostcontainer");
    if (container.style.display != "none") {
        container.style.display = "none";
    } else {
        container.style.display = "block";
    }
}

function shownetworks() {
    var container = document.getElementById("networkcontainer");
    var url = window.location + "/shownetworks";
    var method = "GET";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        var resp = JSON.parse(data);
        var i = 0;
        var obj = 'netname'
        for (i = 0, obj; obj = resp.objects[i]; i++) {
            var p = document.createElement("p");
            var info = document.createTextNode(obj);
            p.appendChild(info);
            container.appendChild(p);
        }
    }
    request.open(method, url);
    request.send();
}

function togglenetworks() {
    var container = document.getElementById("networkcontainer");
    if (container.style.display != "none") {
        container.style.display = "none";
    } else {
        container.style.display = "block";
    }
}
