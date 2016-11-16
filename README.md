XSSER
==========

<a href="https://www.blackhat.com/eu-15/arsenal.html"><img alt="Black Hat Arsenal" src="https://www.toolswatch.org/badges/arsenal/2015.svg" /></a>

<a href="https://www.blackhat.com/eu-16/arsenal.html"><img alt="Black Hat Arsenal" src="https://www.toolswatch.org/badges/arsenal/2016.svg" /></a>

### Presentation
* From XSS to RCE 2.5 - Black Hat Europe Arsenal 2016

### Demo
* Version 2.0 - 2015: https://www.youtube.com/playlist?list=PLIjb28IYMQgqqqApoGRCZ_O40vP-eKsgf
* Version 2.5 - 2016: https://www.youtube.com/playlist?list=PLRic6PgcrsWGkgacL6WFnSQKVRZIoofRj

Requirements
------------
* Python (2.7.*, version 2.7.11 was used for development and demo)
* Gnome
* Bash
* Msfconsole (accessible via environment variables)
* Netcat (nc)
* cURL (curl) [NEW]
* PyGame (apt-get install python-pygame) [NEW]

Payload Compatibility
------------
* Chrome (14 Nov 2015) - This should still work.
* Firefox (04 Nov 2016) - Tested live at Black Hat Arsenal 2016

WordPress Lab
------------------
* WordPress http://wordpress.org/
* Better WP Security 3.5.3 http://www.exploit-db.com/wp-content/themes/exploit/applications/c6d6beb3c11bc58856e15218d512b851-better-wp-security.3.5.3.zip
* Optional: WPSEO https://yoast.com/wordpress/plugins/seo/

WordPress Exploit
------------------
* http://www.exploit-db.com/exploits/27290/

Joomla Lab
------------------
* Joomla https://www.joomla.org/
* SecurityCheck 2.8.9 https://www.exploit-db.com/apps/543ccd00b06d24be139d7e18212a0916-com_securitycheck_j3x-2.8.9.zip

Joomla Exploit
------------------
* https://www.exploit-db.com/exploits/39879/

Directories
------------
* Audio: Contains remixed audio notifications.
* Exploits: Contains DirtyCow (DCOW) privilege escalation exploits.
* Joomla_Backdoor: Contains a sample Joomla extension backdoor which can be uploaded as an administrator and subsequently used to execute arbitrary commands on the system with system($_GET['c']).
* Payloads/javascript: Contains the JavaScript payloads. Contains a new "add new admin" payload for Joomla.
* Shells: Contains the PHP shells to inject, including a slightly modified version of pentestmonkey's shell that connects back via wget.

Developed By
------------
* Hans-Michael Varbaek
* Sense of Security

Credits
------------
* MaXe / InterN0T

Code Design
-----------
* It works! (Again!)
* Spaghetti code
* Just-In-Time for Black Hat Europe 2016
