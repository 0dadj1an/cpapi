function deleteRule(tr) {
    var ruleid = tr.id;
    console.log(ruleid);
}

function editRule(tr) {
    var ruleid = tr.id;
    console.log(ruleid);
}

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
    var rulenumid = 1;
    var currule = "somerule";

    for (i = 0; i < rules.rulebase.length; i++) {
        var rulecontainer = document.createElement("tr");
        currule = rules.rulebase[i];
        if (currule.type === "accesssection") {
            rulecontainer.classList.add("rulesection");
            var nametd = document.createElement("td");
            nametd.colSpan = "9";
            nametd.innerText = currule.name;
            rulecontainer.appendChild(nametd);
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
            numinput.disabled="true";
            numtd.appendChild(numinput);
            //NAME
            var nametd = document.createElement("td");
            var nameinput = document.createElement("input");
            nameinput.name = "name";
            nameinput.type = "text";
            nameinput.disabled="true";
            if (currule.enabled == false) {
                rulecontainer.classList.add("disabledrule");
            }
            nametd.appendChild(nameinput)
            //SOURCE
            var sourcetd = document.createElement("td");
            var br = document.createElement("br");
            for (j = 0; j < rules.rulebase[i].source.length; j++) {
                source = rules.rulebase[i].source[j];
                if (source[0] != "Any") {
                    var sourcea = document.createElement("a");
                    var br = document.createElement("br");
                    sourcea.innerText = source[0];
                    sourcea.href = "/showobject/" + source[1];
                    sourcea.target = "_blank"
                    sourcetd.appendChild(sourcea);
                    sourcetd.appendChild(br);
                } else {
                    sourcea = document.createElement("p");
                    sourcea.innerText = "Any";
                    sourcetd.appendChild(sourcea);
                }
            }
            if (currule["source-negate"] == true) {
                sourcetd.classList.add("negatedcell");
            }
            //DESTINATION
            var destinationtd = document.createElement("td");
            var br = document.createElement("br");
            for (j = 0; j < rules.rulebase[i].destination.length; j++) {
                destination = rules.rulebase[i].destination[j];
                if (destination[0] != "Any") {
                    var destinationa = document.createElement("a");
                    var br = document.createElement("br");
                    destinationa.innerText = destination[0];
                    destinationa.href = "/showobject/" + destination[1];
                    destinationa.target = "_blank"
                    destinationtd.appendChild(destinationa);
                    destinationtd.appendChild(br);
                } else {
                  destinationa = document.createElement("p");
                  destinationa.innerText = "Any";
                  destinationtd.appendChild(destinationa);
                }
            }
            if (currule["destination-negate"] == true) {
                destinationtd.classList.add("negatedcell");
            }
            //SERVICE
            var servicetd = document.createElement("td");
            var br = document.createElement("br");
            for (j = 0; j < rules.rulebase[i].service.length; j++) {
                service = rules.rulebase[i].service[j];
                if (service[0] != "Any") {
                    var servicea = document.createElement("a");
                    var br = document.createElement("br");
                    servicea.innerText = service[0];
                    servicea.href = "/showobject/" + service[1];
                    servicea.target = "_blank"
                    servicetd.appendChild(servicea);
                    servicetd.appendChild(br);
                } else {
                    servicea = document.createElement("p");
                    servicea.innerText = "Any";
                    servicetd.appendChild(servicea);
                }
            }
            if (currule["service-negate"] == true) {
                servicetd.classList.add("negatedcell");
            }
            //ACTION
            var actiontd = document.createElement("td");
            var actionselect = document.createElement("select");
            actionselect.disabled="true";
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
            trackselect.disabled="true";
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
            var br = document.createElement("br");
            for (j = 0; j < rules.rulebase[i].target.length; j++) {
                target = rules.rulebase[i].target[j];
                if (target[0] != "Policy Targets") {
                    var targeta = document.createElement("a");
                    var br = document.createElement("br");
                    targeta.innerText = target[0];
                    targeta.href = "/showobject/" + target[1];
                    targeta.target = "_blank"
                    targettd.appendChild(targeta);
                    targettd.appendChild(br);
                } else {
                    targeta = document.createElement("p");
                    targeta.innerText = "Policy Targets";
                    targettd.appendChild(targeta);
                }
            }
            //EDIT
            var modifytd = document.createElement("td");
            var deleteinput = document.createElement("input");
            var editinput = document.createElement("input");
            deleteinput.setAttribute("onclick","javascript:deleteRule(this);");
            deleteinput.id = rulenumid;
            deleteinput.name = "delete";
            deleteinput.type = "image";
            deleteinput.value = "delete";
            deleteinput.src = "/static/files/delete.png";
            editinput.setAttribute("onclick","javascript:editRule(this);");
            editinput.id = rulenumid;
            editinput.name = "edit";
            editinput.type = "image";
            editinput.value = "edit";
            editinput.src = "/static/files/edit.png";
            modifytd.appendChild(deleteinput);
            modifytd.appendChild(editinput);
            //ADD ALL TD TO CONTAINER TR
            rulecontainer.appendChild(numtd);
            rulecontainer.appendChild(nametd);
            rulecontainer.appendChild(sourcetd);
            rulecontainer.appendChild(destinationtd);
            rulecontainer.appendChild(servicetd);
            rulecontainer.appendChild(actiontd);
            rulecontainer.appendChild(tracktd);
            rulecontainer.appendChild(targettd);
            rulecontainer.appendChild(modifytd);
            rulenumid += 1;
        }
        tbody.appendChild(rulecontainer);
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

function objectdisplay(local, remote) {
    var h4 = document.getElementById("synch4");
    var image = document.getElementById("syncimage");
    if (local === remote) {
        h4.innerText = "Database Synced     ";
        image.src = "/static/files/check.png"
    } else if (local === 0) {
        h4.innerText = "Need Full Sync     ";
        image.src = "/static/files/fullsync.png";
    } else if (local != remote) {
        h4.innerText = "Delta sync in progress...     ";
        image.src = "/static/files/syncing.png";
    }
}

function objectupdate() {
    var currentwindow = window.location.href;
    var url = window.location.origin + "/objects/objectcheck";
    var method = "GET";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        var resp = JSON.parse(data);
        if (currentwindow.includes("objects")) {
            var local = document.getElementById("local");
            var remote = document.getElementById("remote");
            local.innerText = resp.local;
            remote.innerText = resp.remote;
        }
        if (resp.local != 0) {
            if (resp.local != resp.remote) {
                deltasync();
            }
        } else {
              if (currentwindow.includes("objects")) {
              fullsync();
            }
        }
        objectdisplay(resp.local, resp.remote);
    }
    request.open(method, url);
    request.send();
}

setInterval(objectupdate, 10000);

function deltasync() {
    var url = window.location.origin + "/objects/deltasync";
    var method = "GET";
    var request = new XMLHttpRequest();
    request.onload = function() {
        var status = request.status;
        var data = request.responseText;
        if (currentwindow.includes("objects")) {
            showobjects();
        }
    }
    request.open(method, url);
    request.send();
}

function fullsync() {
    var h4 = document.getElementById("synch4");
    var image = document.getElementById("syncimage");
    h4.innerText = "Full sync in progress...";
    image.src = "/static/files/syncing.png";
    var url = window.location.href + "/fullsync";
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
    var currentwindow = window.location.href;
    if (currentwindow.includes("objects")) {
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
    var url = window.location.href + "/showhosts";
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
    var url = window.location.href + "/shownetworks";
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
    var url = window.location.href + "/showgroups";
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
    var url = window.location.href + "/showaccessroles";
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
    var url = window.location.href + "/showservers";
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
    var url = window.location.href + "/showservices";
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
var currentwindow = window.location.href;
if (currentwindow.includes("objects")) {
    showhosts();
    shownetworks();
    showgroups();
    showaccessroles();
    showservers();
    showservices();
}
