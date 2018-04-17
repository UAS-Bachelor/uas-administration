function changeVisibility(divId, choiceId, name) {
    var div = document.getElementById(divId)
    var chosen = document.getElementById(choiceId)
    var choices = document.getElementsByClassName(name)

    for (var i = 0; i < choices.length; i++) {
        choices[i].style.display = 'none'
    }
    if (chosen.checked) {
        div.style.display = 'block'
    }
}

function resetInputs(parent) {
}

function submitMission(rootId) {
    var childElements = document.getElementById(rootId).elements;
    for (var i = 0; i < childElements.length; i++) {
        var type = childElements[i].getAttribute("type");

        console.log(childElements[i]);
        console.log(childElements[i].getAttribute("type"));
        console.log("");
    }
    validateSubmit(rootId)
}

function validateSubmit(rootId) {
    var id = "#"+rootId;
    var valuesToSubmit = { errors: false};
    validateChildren(id, valuesToSubmit);
    console.log(valuesToSubmit);

    if(valuesToSubmit.errors) {
        document.getElementById("errorMessage").style.display = "block";
    }
    else {

    }
    sendData();
}

function sendData() {
    var formData = new FormData();
    var input = document.getElementsByName("upload-file-SORA")[0];

    formData.append("sora", input.files[0]);

    //console.log(formData);
    var request = new XMLHttpRequest();
    request.open("POST", "/save-mission");
    request.send(formData);
}

function validateChildren(parent, valuesToSubmit) {
    var errors = false;
    $(parent).children().filter("div").each(function () {
        var children = $(this).children().filter("input");
        console.log("Children: " + children.attr("type") + " " + children.attr("name"));
        if (children.attr("type") === "radio") {
            errors = (errors ? true : !validateRadio(children.attr("name"), valuesToSubmit));
        }
        else if (children.attr("type") === "file") {
            validateFile(children.attr("name"), valuesToSubmit);
        }
    });
}

function validateRadio(name, valuesToSubmit) {
    var radioButtons = document.getElementsByName(name);
    var anyChecked = false;
    for (var i = 0; i < radioButtons.length; i++) {
        if (radioButtons[i].checked === true) {
            anyChecked = true;
            var modeLength = radioButtons[i].getAttribute("name").length;
            var chosenId = "#" + radioButtons[i].getAttribute("id").substr(modeLength);
            validateChildren(chosenId);
        }
    }
    return anyChecked;
}

function validateFile(name, valuesToSubmit) {
    var file = document.getElementsByName(name)[0];
    if (file.value === "") {
        valuesToSubmit.errors = true;
    }
    else {
        valuesToSubmit[name] = file.value;
    }
}