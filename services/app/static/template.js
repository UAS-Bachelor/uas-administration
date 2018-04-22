function changeVisibility(divId, choiceId, name) {
    let div = document.getElementById(divId)
    let chosen = document.getElementById(choiceId)
    let choices = document.getElementsByClassName(name)

    for (let i = 0; i < choices.length; i++) {
        choices[i].style.display = 'none'
    }
    if (chosen.checked) {
        div.style.display = 'block'
    }
}

function resetInputs(parent) {
}

function validateSubmit(rootId) {
    document.getElementById("errorMessage").style.display = "none";
    document.getElementById("serverErrorMessage").style.display = "none";
    document.getElementById("successMessage").style.display = "none";

    let id = "#" + rootId;
    let valuesToSubmit = {errors: false};
    validateChildren(id, valuesToSubmit);

    if (valuesToSubmit.errors) {
        document.getElementById("errorMessage").style.display = "block";
    }
    else {
        delete valuesToSubmit.errors;
        sendData(valuesToSubmit);
    }
}

function sendData(valuesToSend) {
    let formData = new FormData();

    for (const [key, value] of Object.entries(valuesToSend)) {
        if (value instanceof HTMLInputElement) {
            let file = value.files[0];
            formData.append(key, file);
        }
        else {
            formData.append(key, value);
        }
    }

    let request = new XMLHttpRequest();
    request.onreadystatechange = function () {
        if (request.readyState === 4) {
            let result = JSON.parse(request.response);
            if (result.result) {
                document.getElementById("successMessage").style.display = "block";
            }
            else {
                document.getElementById("serverErrorMessage").style.display = "block";
            }
        }
    };
    request.open("POST", "http://127.0.0.1:5004/save-mission");
    request.send(formData);
}

function validateChildren(parent, valuesToSubmit) {
    $(parent).children().filter("div").each(function () {
        let id = $(this).attr("id");
        if (id === "map") {
            validateMap(valuesToSubmit);
        }
        else {
            let children = $(this).children().filter("input");
            //console.log("Children: " + children.attr("type") + " " + children.attr("name") + " " + children.prop("tagName"));
            if (children.attr("type") === "radio") {
                validateRadio(children.attr("name"), valuesToSubmit);
            }
            else if (children.attr("type") === "file") {
                validateFile(children.attr("id"), valuesToSubmit);
            }

            else if (children.attr("type") === "text") {
                validateText(children.attr("id"), valuesToSubmit);
            }
        }
    });
}

function validateText(id, valuesToSubmit) {
    let file = document.getElementById(id);
    if (file.value === "") {
        valuesToSubmit.errors = true;
    }
    else {
        valuesToSubmit[file.name] = file.value;
    }
}

function validateMap(valuesToSubmit) {
    let feature = source.getFeatureById(flightId);
    if((feature == null)) {
        valuesToSubmit.errors = true;
    }
    else {
        let zone = feature.getGeometry();
        let mapDetails = {};
        mapDetails.center = zone.getCenter();
        mapDetails.radius = zone.getRadius();
        mapDetails.bufferSize = bufferSize;
        valuesToSubmit.map = JSON.stringify(mapDetails);
    }
}

function validateRadio(name, valuesToSubmit) {
    let radioButtons = document.getElementsByName(name);
    let anyChecked = false;
    for (let i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked === true) {
            anyChecked = true;
            let modeLength = radioButtons[i].getAttribute("name").length;
            let chosen = radioButtons[i].getAttribute("id").substr(modeLength)
            let chosenId = "#" + chosen;
            valuesToSubmit[name] = chosen;
            validateChildren(chosenId, valuesToSubmit);
        }
    }
    if (!anyChecked) {
        valuesToSubmit.errors = true;
    }
}

function validateFile(id, valuesToSubmit) {
    let file = document.getElementById(id);
    if (file.value === "") {
        valuesToSubmit.errors = true;
    }
    else {
        valuesToSubmit[file.name] = file;
    }
}