var Pluma = function (options) {
	this.options = options || {};
};

Pluma.prototype = {
		
	initComposer : function (container_id, textarea_id, form_id) {
		if (this.editor == undefined) {
			var p = this;
			
			// Replace textarea now that JavaScript is verified as enabled
			var composer = $('#' + container_id);
			var basic_composer = $('#' + textarea_id);
			composer.attr('style', basic_composer.attr('style')); 	// copy style
			basic_composer.hide();									// hide basic
			composer.html(basic_composer.html());					// copy contents
			
			this.editor = editor = ace.edit(container_id);
		    editor.setTheme("ace/theme/eclipse");
		    $('#type_select').change(function (event) {
		    	p.setEditorMode($(event.currentTarget).val());
		    });
		    
		    $('#' + form_id).submit(function () {
		    	basic_composer.text(editor.getSession().getValue());
		    });
		    
		    $('input, textarea').attr('tabindex', 1);
		    $('input[name=title]').focus();
		}
	},
	
	init : function () {
	},
	
	_script : function (path) {
		var script = document.createElement('script');
		script.src = path;
		script.type = 'text/javascript';
		document.body.appendChild(script);
	},
	
	setEditorMode : function (mode_name) {
		if (this.editor != undefined) {
			if (mode_name == 'html' || mode_name == 'css' || mode_name == 'javascript') {
				// mode_name is valid
	    	} else {
	    		mode_name = 'text';
	    	}
			var Mode = require("ace/mode/" + mode_name).Mode;
			this.editor.getSession().setMode(new Mode());
		}
	},
	
	resizeInboxDoc : function (iframe_id) {
		var doc = document.getElementById(iframe_id);
		doc.height = doc.contentWindow.document.body.scrollHeight;
		doc.width = doc.contentWindow.document.body.scrollWidth;
	},
};
