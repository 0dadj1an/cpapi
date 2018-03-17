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
    var url = window.location + "/deltasync";
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

function objectsearch() {
    var outpute = document.getElementById("filtercontainer");
    while (outpute.firstChild) {
      outpute.removeChild(outpute.firstChild);
    }
    var string = document.getElementById("searchstring").value;
    if (string == '') {
        return;
    }
    var para = document.getElementsByTagName("p");
    var curp = "currentpara";
    for (var i = 0; i < para.length; i++) {
        curp = para[i]
        var data = curp.innerText;
        if (data.includes(string)) {
            var br = document.createElement("br");
            var label = document.createElement("label");
            var match = document.createTextNode(data);
            label.appendChild(match);
            outpute.appendChild(label);
            outpute.appendChild(br)
        }
    }
}

function showobjects() {
    showhosts();
    shownetworks();
    showgroups();
    showaccessroles();
    showservers();
    showservices();
}

function showhosts() {
    var container = document.getElementById("hostscontainer");
    while (container.firstChild) {
      container.removeChild(container.firstChild);
    }
    var url = window.location + "/showhosts";
    var method = "GET";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        var resp = JSON.parse(data);
        var i = 0;
        var obj = 'hostname'
        for (i = 0; obj = resp.objects[i]; i++) {
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
    var container = document.getElementById("hostscontainer");
    if (container.style.display != "none") {
        container.style.display = "none";
    } else {
        container.style.display = "block";
    }
}

function shownetworks() {
    var container = document.getElementById("networkscontainer");
    while (container.firstChild) {
      container.removeChild(container.firstChild);
    }
    var url = window.location + "/shownetworks";
    var method = "GET";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        var resp = JSON.parse(data);
        var i = 0;
        var obj = 'netname'
        for (i = 0; obj = resp.objects[i]; i++) {
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
    var container = document.getElementById("networkscontainer");
    if (container.style.display != "none") {
        container.style.display = "none";
    } else {
        container.style.display = "block";
    }
}

function showgroups() {
    var container = document.getElementById("groupscontainer");
    while (container.firstChild) {
      container.removeChild(container.firstChild);
    }
    var url = window.location + "/showgroups";
    var method = "GET";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        var resp = JSON.parse(data);
        var i = 0;
        var obj = 'groupname'
        for (i = 0; obj = resp.objects[i]; i++) {
            var p = document.createElement("p");
            var info = document.createTextNode(obj);
            p.appendChild(info);
            container.appendChild(p);
        }
    }
    request.open(method, url);
    request.send();
}

function togglegroups() {
    var container = document.getElementById("groupscontainer");
    if (container.style.display != "none") {
        container.style.display = "none";
    } else {
        container.style.display = "block";
    }
}

function showaccessroles() {
    var container = document.getElementById("accessrolescontainer");
    while (container.firstChild) {
      container.removeChild(container.firstChild);
    }
    var url = window.location + "/showaccessroles";
    var method = "GET";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        var resp = JSON.parse(data);
        var i = 0;
        var obj = 'accessrolename'
        for (i = 0; obj = resp.objects[i]; i++) {
            var p = document.createElement("p");
            var info = document.createTextNode(obj);
            p.appendChild(info);
            container.appendChild(p);
        }
    }
    request.open(method, url);
    request.send();
}

function toggleaccessroles() {
    var container = document.getElementById("accessrolescontainer");
    if (container.style.display != "none") {
        container.style.display = "none";
    } else {
        container.style.display = "block";
    }
}

function showservers() {
    var container = document.getElementById("serverscontainer");
    while (container.firstChild) {
      container.removeChild(container.firstChild);
    }
    var url = window.location + "/showservers";
    var method = "GET";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        var resp = JSON.parse(data);
        var i = 0;
        var obj = 'servername'
        for (i = 0; obj = resp.objects[i]; i++) {
            var p = document.createElement("p");
            var info = document.createTextNode(obj);
            p.appendChild(info);
            container.appendChild(p);
        }
    }
    request.open(method, url);
    request.send();
}

function toggleservers() {
    var container = document.getElementById("serverscontainer");
    if (container.style.display != "none") {
        container.style.display = "none";
    } else {
        container.style.display = "block";
    }
}

function showservices() {
    var container = document.getElementById("servicescontainer");
    while (container.firstChild) {
      container.removeChild(container.firstChild);
    }
    var url = window.location + "/showservices";
    var method = "GET";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        var resp = JSON.parse(data);
        var i = 0;
        var obj = 'servicename'
        for (i = 0; obj = resp.objects[i]; i++) {
            var p = document.createElement("p");
            var info = document.createTextNode(obj);
            p.appendChild(info);
            container.appendChild(p);
        }
    }
    request.open(method, url);
    request.send();
}

function toggleservices() {
    var container = document.getElementById("servicescontainer");
    if (container.style.display != "none") {
        container.style.display = "none";
    } else {
        container.style.display = "block";
    }
}
