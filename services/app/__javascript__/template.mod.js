	(function () {
		var __name__ = '__main__';
		var HandleRadioButtons = __class__ ('HandleRadioButtons', [object], {
			__module__: __name__,
			get test () {return __get__ (this, function (self, divId, choiceId, py_name) {
				var div = document.getElementById (divId);
				var chosen = document.getElementById (choiceId);
				var choices = document.getElementsByClassName (py_name);
				var __iterable0__ = choices;
				for (var __index0__ = 0; __index0__ < len (__iterable0__); __index0__++) {
					var choice = __iterable0__ [__index0__];
					choice.style.display = 'none';
				}
				if (chosen.checked) {
					div.style.display = 'block';
				}
			});}
		});
		var handleRadioButtons = HandleRadioButtons ();
		__pragma__ ('<all>')
			__all__.HandleRadioButtons = HandleRadioButtons;
			__all__.__name__ = __name__;
			__all__.handleRadioButtons = handleRadioButtons;
		__pragma__ ('</all>')
	}) ();
