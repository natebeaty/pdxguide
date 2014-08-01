// PAGINATOR FUNCTION FOR DJANGO PAGINATOR.HTML TAG
var Paginator =
{
    jumpToPage: function(pages,q)
    {
        var page = prompt("Enter a number between 1 and " + pages + " to jump to that page", "");
        if (page != undefined)
        {
            page = parseInt(page, 10)
            if (!isNaN(page) && page > 0 && page <= pages)
            {
                window.location.href = "?q="+q+"&page=" + page;
            }
        }
    }
};

function fieldClear(fieldTxt,txt) { 
	if (fieldTxt.value == txt) fieldTxt.value = "";
	}

function fieldRestore(fieldTxt,txt) { 
	if (fieldTxt.value == "") fieldTxt.value = txt;
	}

function PopupPic(sPicURL,sPicTitle) {
	window.open('/popup.php?file='+sPicURL+'&title='+sPicTitle,"vd_blowup","height=400,width=400,scrollbars=0,resizable=1");
} 

function PopupWindow(sURL,sW,sH) {
	window.open(sURL,"PopupWindow5000","height="+sH+",width="+sW+",scrollbars=1,resizable=1");
} 

function makeEmailLink(address, text) {
	document.write('<a href="mailto:' + address + '">' + text + '</a>');
	}

//     ------------------------------------
//     STANDARDS-COMPLIANT EXTERNAL LINKS
//     ------------------------------------

function convertExternalLinks () {
	var links = document.getElementsByTagName('a');

	for (var i = links.length; i != 0; i--) {		
		var a = links[i-1];

		if (!a.href) continue;
		if (a.className && a.className.indexOf('external') != -1) a.target = '_blank';
	}
}

/* Nate's mootools functions for generic form validation */

// Tries to get field name from <label>, resorts to capitalized version of 
function getFieldName(field) {
    if ($(field.id+'-label')) {
        var fieldStr = $(field.id+'-label').innerHTML;
        // strip out <input /> tags (if the <input> is inside the <label> as it is in comments.php)
        fieldStr = fieldStr.replace(/<input[^>]+\/?>/g,'');
        // strip out <span>foo</span> fields and whatnot, such as (required) (not shown) in comments form
        fieldStr = fieldStr.replace(/<[^>]+>[^<]+<[^>]+>/g,'').trim();
        // strip out colons
        fieldStr = fieldStr.replace(/:$/g,'');
    } else {
        // use field's name if <label> can't be found
        var fieldStr = field.name.replace(/-/g,' ').trim().capitalize();
    }
    return fieldStr;
}

function isEmail(str) {
       var isEmail  = /^([a-zA-Z0-9_\.\-])+\@(([a-zA-Z0-9\-])+\.)+([a-zA-Z0-9]{2,4})+$/;
	return isEmail.test(str);
}

/*  Simple form validator -- checks for inputs with class 'required' -- also validates field 'email' if present */

function checkForm(formToCheck) {
	var errorReturn = '';
	var focusAfter = '';

	var reqFields = $(formToCheck).getElements('.required-field');
	reqFields.forEach(function(field){
		if (field.value.trim() == '') {
			focusAfter = (focusAfter == '') ? field : focusAfter; // Set focus to first error after check
			errorReturn += 'Please enter a value for ' + getFieldName(field) + ".\n";
		}
	});	
       
	var emailFields = $(formToCheck).getElements('.isEmail');
	emailFields.forEach(function(field){
   		if (!isEmail(field.value))
   		{
   			focusAfter = (focusAfter == '') ? field : focusAfter;
   			errorReturn += 'Please enter a valid email for ' + getFieldName(field) + ".\n";
   		}
    });	
	
	if (errorReturn != '')
	{
		alert(errorReturn);
		focusAfter.focus();
		return false;
	} else {
		return true;
	}
}


// CONVERT EXTERNAL LINKS ON PAGE
window.addEvent('domready', function() {
    convertExternalLinks();
    
});
window.addEvent('load', function() {
    _uacct = "UA-248215-3";
    urchinTracker();
});