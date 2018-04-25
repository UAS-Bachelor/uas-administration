function changeVisibilityRadio(divId, choiceId, name) {
    let div = document.getElementById(divId)
    let chosen = document.getElementById(choiceId)
    let choices = document.getElementsByClassName(name)

    for (let i = 0; i < choices.length; i++) {
        choices[i].style.display = 'none'
    }
    if (chosen.checked) {
        div.style.display = 'block';
    }
}

function changeVisibilityCheckbox(divId, checkboxId) {
    let div = document.getElementById(divId);
    let checkbox = document.getElementById(checkboxId);

    if (checkbox.checked) {
        div.style.display = 'block';
    }
    else {
        div.style.display = 'none';
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
    //request.open("POST", "http://127.0.0.1:5004/save-mission");
    //request.send(formData);
}

function validateChildren(parent, valuesToSubmit) {
    $(parent).children().filter("div").each(function () {
        let id = $(this).attr("id");
        if (id === "map-requirement") {
            validateMap($(this).attr("name"), valuesToSubmit);
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

            else if (children.attr("type") === "checkbox") {
                validateCheckbox(children.attr("id"), valuesToSubmit);
            }

            let mutliLineText = $(this).children().filter("textarea");

            if (mutliLineText.attr("name") === "multiline") {
                validateMultilineText(mutliLineText.attr("id"), valuesToSubmit)
            }
        }
    });
}

function validateCheckbox(id, valuesToSubmit) {
    let checkbox = document.getElementById(id);
    if (checkbox.checked) {
        let divWithChildren = "#" + id + "-children-div";
        validateChildren(divWithChildren, valuesToSubmit);
    }
}

function validateText(id, valuesToSubmit) {
    let textField = document.getElementById(id);
    if (textField.value === "") {
        valuesToSubmit.errors = true;
    }
    else {
        valuesToSubmit[textField.name] = textField.value;
    }
}

function overlapWithNoFlight(name) {
    console.log(name);
    let div = document.getElementById('map-requirement');
    div.style.display = 'block';
    div.getElementsByTagName("P")[0].innerHTML = name;
}

function resetMapRequirement() {
    let div = document.getElementById('map-requirement');
    div.style.display = 'none';
}

function validateMap(name, valuesToSubmit) {
    //let feature = source.getFeatureById(flightId);
    let fileElementName = "map-overlap-" + name;
    let file = document.getElementById(fileElementName);
    if (flightZoneIsNotDrawn()) {
        valuesToSubmit.errors = true;
    }
    else if ($('#map-requirement').is(':visible')) {
        if (file.value === "") {
            valuesToSubmit.errors = true;
        }
    }
    else {/*
        let zone = feature.getGeometry();
        let mapDetails = {};
        mapDetails.center = zone.getCenter();
        mapDetails.radius = zone.getRadius();
        mapDetails.bufferSize = bufferSize;*/
        valuesToSubmit.map = JSON.stringify(getMapDetails());
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

function validateMultilineText(id, valuesToSubmit) {
    let text = document.getElementById(id).value;
    valuesToSubmit["Comment"] = text;
}