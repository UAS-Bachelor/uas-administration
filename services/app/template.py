class HandleRadioButtons:
    
    def test(self, divId, choiceId, name):
        
        div = document.getElementById(divId)
        chosen = document.getElementById(choiceId)
        choices = document.getElementsByClassName(name)

        for choice in choices:
            choice.style.display = 'none'

        if chosen.checked:
            div.style.display = 'block'

handleRadioButtons = HandleRadioButtons()