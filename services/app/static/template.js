function changeVisibility(divId, choiceId, name) {
    var div = document.getElementById(divId)
    var chosen = document.getElementById(choiceId)
    var choices = document.getElementsByClassName(name)

    for (i = 0; i < choices.length; i++){
        choices[i].style.display = 'none'
    }
    if (chosen.checked) {
        div.style.display = 'block'
    }
}