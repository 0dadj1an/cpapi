function dislplayrules(rules, offset) {
    var ruletable = document.getElementById("ruletable");
    ruletable.style.display = "block";
    var tbody = document.getElementById("tbody");
    if (offset === 0) {
      while (tbody.firstChild) {
        tbody.removeChild(tbody.firstChild);
      }
    }
    var i = 0;
    var currule = "somerule";

    for (i = 0; i < rules.rulebase.length; i++) {
        var rulecontainer = document.createElement("tr");
        currule = rules.rulebase[i];
        if (currule.type === "accessection") {
            rulecontainer.classList.add("rulesection");
            var nametd = document.createElement("td");
            nametd.classList.add("namediv");
            var nameinput = document.createElement("input");
            nameinput.name = "name";
            nameinput.type = "text";
            nameinput.value = currule.name;
            nametd.appendChild(nameinput);
        } else if (currule.type === "accessrule") {
            var j = 0;
            //NUMBER
            var numtd = document.createElement("td");
            if (currule.enable === "true") {
                rulecontainer.classList.add("disabledrule");
            }
            var numinput = document.createElement("input");
            numinput.name = "position";
            numinput.type = "text";
            numinput.value = currule.number;
            numtd.appendChild(numinput);
            //NAME
            var nametd = document.createElement("td");
            var nameinput = document.createElement("input");
            nameinput.name = "name";
            nameinput.type = "text";
            nameinput.value = currule.name;
            nametd.appendChild(nameinput)
            //SOURCE
            var sourcetd = document.createElement("td");
            var sourceselect = document.createElement("select")
            sourceselect.classList.add("selectjs")
            sourceselect.name = "source"
            sourceselect.multiple = "multiple";
            sourceselect.type = "text";
            for (j = 0; j < rules.rulebase[i].source.length; j++) {
                source = rules.rulebase[i].source[j];
                var newopt = document.createElement("option");
                newopt.text = source[0];
                newopt.value = source[1];
                sourceselect.add(newopt);
            }
            sourcetd.appendChild(sourceselect);
            //DESTINATION
            var destinationtd = document.createElement("td");
            var destinationselect = document.createElement("select");
            destinationselect.name = "destination";
            destinationselect.multiple = "multiple";
            destinationselect.type = "text";
            for (j = 0; j < rules.rulebase[i].destination.length; j++) {
                destination = rules.rulebase[i].destination[j];
                var newopt = document.createElement("option");
                newopt.text = destination[0];
                newopt.value = destination[1];
                destinationselect.add(newopt);
            }
            destinationtd.appendChild(destinationselect);
            //SERVICE
            var servicetd = document.createElement("td");
            var serviceselect = document.createElement("select");
            serviceselect.name = "service";
            serviceselect.multiple = "multiple";
            serviceselect.type = "text";
            for (j = 0; j < rules.rulebase[i].service.length; j++) {
                service = rules.rulebase[i].service[j];
                var newopt = document.createElement("option");
                newopt.text = service[0];
                newopt.value = service[1];
                serviceselect.add(newopt);
            }
            servicetd.appendChild(serviceselect);
            //ACTION
            var actiontd = document.createElement("td");
            var actionselect = document.createElement("select");
            actionselect.name = "action";
            actionselect.type = "text";
            var acceptopt = document.createElement("option");
            var dropopt = document.createElement("option");
            acceptopt.text = "Accept";
            acceptopt.value = "accept";
            dropopt.text = "Drop";
            dropopt.value = "drop";
            actionselect.add(acceptopt);
            actionselect.add(dropopt);
            actiontd.appendChild(actionselect);
            //TRACK
            var tracktd = document.createElement("td");
            var trackselect = document.createElement("select");
            trackselect.name = "track";
            trackselect.type = "text";
            var noneopt = document.createElement("option");
            var logopt = document.createElement("option");
            var extopt = document.createElement("option");
            var detopt = document.createElement("option");
            noneopt.text = "None";
            noneopt.value = "none";
            logopt.text = "Log";
            logopt.value = "Log";
            extopt.text = "Extended Log";
            extopt.value = "Extended Log";
            detopt.text = "Detailed Log";
            detopt.value = "Detailed Log";
            trackselect.add(noneopt);
            trackselect.add(logopt);
            trackselect.add(extopt);
            trackselect.add(detopt);
            tracktd.appendChild(trackselect);
            //TARGET
            var targettd = document.createElement("td");
            var targetselect = document.createElement("select");
            targetselect.name = "target";
            targetselect.multiple = "multiple";
            targetselect.type = "text";
            for (j = 0; j < rules.rulebase[i].target.length; j++) {
                target = rules.rulebase[i].target[j];
                var newopt = document.createElement("option");
                newopt.text = target[0];
                newopt.value = target[1];
                targetselect.add(newopt);
            }
            targettd.appendChild(targetselect);
            //EDIT
            var edittd = document.createElement("td");
            var editinput = document.createElement("input");
            editinput.name = "delete";
            editinput.type = "image";
            editinput.value = "add";
            editinput.src = "/static/files/delete.png";
            edittd.appendChild(editinput);
            //ADD ALL DIVS TO CONTAINER
            rulecontainer.appendChild(numtd);
            rulecontainer.appendChild(nametd);
            rulecontainer.appendChild(sourcetd);
            rulecontainer.appendChild(destinationtd);
            rulecontainer.appendChild(servicetd);
            rulecontainer.appendChild(actiontd);
            rulecontainer.appendChild(tracktd);
            rulecontainer.appendChild(targettd);
            rulecontainer.appendChild(edittd);
            //ADD RULECONTAINER TO TABLE
            tbody.appendChild(rulecontainer);
        }
    }
}

function showpolicyPost(offset = 0) {
    var url = window.location.href + "/showrules";
    var method = "POST";
    var postData = {};
    var layeruid = document.getElementById("layer").value;
    var prog = document.getElementById("policyprogress");
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        var allrules = JSON.parse(data);
        dislplayrules(allrules, offset);
        var to = allrules.to.toString();
        var total = allrules.total.toString();
        prog.innerText = "Loading " + to + " of " + total + " rules.";
        if (allrules.to != allrules.total) {
            document.getElementById("layer").disabled=true;
            offset = offset + 50;
            showpolicyPost(offset);
        } else {
            document.getElementById("layer").disabled=false;
            prog.innerText = "Loaded " + to + " of " + total + " rules.";
        }
    }
    postData["uid"] = layeruid;
    postData["limit"] = 50;
    postData["offset"] = offset;
    request.open(method, url);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(JSON.stringify(postData));
}

function sandboxPost() {
    var url = window.location.href;
    var method = "POST";
    var postData = {};
    var command = document.getElementById("command").value;
    var payload = document.getElementById("payload").value;
    var element = document.getElementById("sandboxresponse");
    while (element.firstChild) {
      element.removeChild(element.firstChild);
    }
    element.style.display = "none";
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
        element.style.display = "block";
    }
    postData["command"] = command;
    postData["payload"] = payload;
    request.open(method, url);
    request.setRequestHeader("Content-Type", "application/json;charset=UTF-8");
    request.send(JSON.stringify(postData));
}

function objectupdate() {
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
            if (window.location.includes("objects")) {
              fullsync();
            } else {
                console.log('need full sync.')
                //display sync status on pages
                //notify user to perform first full sync on objects page.
            }
        }
    }
    request.open(method, url);
    request.send();
}

setInterval(objectupdate, 10000);

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
    var legend = document.getElementById("resultstotal");
    while (outpute.firstChild) {
      outpute.removeChild(outpute.firstChild);
    }
    var string = document.getElementById("searchstring").value;
    if (string == '') {
        legend.innerText = "Results - 0";
        return;
    }
    var para = document.getElementsByTagName("p");
    var curp = "currentpara";
    var total = 0;
    for (var i = 0; i < para.length; i++) {
        curp = para[i]
        var data = curp.innerText;
        if (data.includes(string)) {
            total += 1;
            var br = document.createElement("br");
            var label = document.createElement("label");
            var match = document.createTextNode(data);
            label.appendChild(match);
            outpute.appendChild(label);
            outpute.appendChild(br);
            legend.innerText = "Results - " + total;
        }
    }
    if (total === 0) {
        legend.innerText = "Results - 0";
    }
}

function showobjects() {
    objectupdate();
    if (window.location.includes("objects")) {
        showhosts();
        shownetworks();
        showgroups();
        showaccessroles();
        showservers();
        showservices();
    }
}

function showhosts() {
    var container = document.getElementById("hostscontainer");
    var legend = document.getElementById("hoststotal");
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
        legend.innerText = "Hosts - " + resp["total"];
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
    var legend = document.getElementById("networkstotal");
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
        legend.innerText = "Networks - " + resp["total"];
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
    var legend = document.getElementById("groupstotal");
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
        legend.innerText = "Groups - " + resp["total"];
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
    var legend = document.getElementById("accessrolestotal");
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
        legend.innerText = "Access-Roles - " + resp["total"];
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
    var legend = document.getElementById("serverstotal");
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
        legend.innerText = "Servers - " + resp["total"];
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
    var legend = document.getElementById("servicestotal");
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
        legend.innerText = "Services - " + resp["total"];
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

objectupdate();
if (window.location.includes("objects")) {
    showhosts();
    shownetworks();
    showgroups();
    showaccessroles();
    showservers();
    showservices();
}
