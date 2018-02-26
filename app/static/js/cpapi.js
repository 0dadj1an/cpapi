function hidehost() {
    var form = document.getElementById("hostform");
    if (form.style.display == "none") {
        form.style.display = "block";
    } else if (form.style.display == "block") {
        form.style.display = "none";
    } else {
        form.style.display = "block";
    }
}

function hidenet() {
    var form = document.getElementById("netform");
    if (form.style.display == "none") {
        form.style.display = "block";
    } else if (form.style.display == "block") {
        form.style.display = "none";
    } else {
        form.style.display = "block";
    }
}

function hidegroup() {
    var form = document.getElementById("groupform");
    if (form.style.display == "none") {
        form.style.display = "block";
    } else if (form.style.display == "block") {
        form.style.display = "none";
    } else {
        form.style.display = "block";
    }
}

function rulesearch() {
    var string = document.getElementById("searchstring").value;
    var table = document.getElementById("tbody");
    for (var i = 0, row; row = table.rows[i]; i++) {
        for (var j = 0, col; col = row.cells[j]; j++) {
            data = col.innerHTML;
            if (data.includes(string)) {
                console.log('Match')
                row.removeAttribute("style");
                break;
            } else {
                console.log('No Match')
                row.style.display = "none";
            }
        }
    }
}
