	(function () {
		var __name__ = '__main__';
		var HandleRadioButtons = __class__ ('HandleRadioButtons', [object], {
			__module__: __name__,
			get test () {return __get__ (this, function (self) {
				document.getElementById ('test').style.display ('block');
			});}
		});
		var handleRadioButtons = HandleRadioButtons ();
		__pragma__ ('<all>')
			__all__.HandleRadioButtons = HandleRadioButtons;
			__all__.__name__ = __name__;
			__all__.handleRadioButtons = handleRadioButtons;
		__pragma__ ('</all>')
	}) ();
