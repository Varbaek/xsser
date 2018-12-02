XSSER
==========

<a href="https://www.blackhat.com/eu-15/arsenal.html"><img alt="Black Hat Arsenal" src="https://github.com/Varbaek/xsser/blob/master/Graphics/badges/blackhat-europe-2015.svg" /></a>

<a href="https://www.blackhat.com/eu-16/arsenal.html"><img alt="Black Hat Arsenal" src="https://github.com/Varbaek/xsser/blob/master/Graphics/badges/blackhat-europe-2016.svg" /></a>

<a href="https://www.blackhat.com/eu-17/arsenal.html"><img alt="Black Hat Arsenal" src="https://github.com/Varbaek/xsser/blob/master/Graphics/badges/blackhat-europe-2017.svg" /></a>

<a href="https://www.blackhat.com/eu-18/arsenal/schedule/index.html"><img alt="Black Hat Arsenal" src="#Not_Available_Yet" /></a>

### Presentation
* From XSS to RCE 2.75 - Black Hat Europe Arsenal 2017

### Demo
* Version 2.0  - 2015: https://www.youtube.com/playlist?list=PLIjb28IYMQgqqqApoGRCZ_O40vP-eKsgf
* Version 2.5  - 2016: https://www.youtube.com/playlist?list=PLRic6PgcrsWGkgacL6WFnSQKVRZIoofRj
* Version 2.75 - 2017: None Currently Available 

Requirements
------------
* Python (2.7.*, version `2.7.14` was used for development and testing)
* Msfconsole (accessible via environment variables)
* Netcat (nc)
* PyGame (pip install pygame)
* jsmin (new dependency - pip install jsmin)
* xterm (previously gnome and bash)

To install the Python dependencies, you can run the following command:

`pip install -r requirements.txt`

If you're using a virtual environment, then you may need to use the full list:

`pip install -r requirements-all-libraries-used.txt`

For installation instructions on Ubuntu 16.04.1 LTS, please refer to the wiki: https://github.com/Varbaek/xsser/wiki

Removed Dependencies:
------------
* Gnome (switched to xterm)
* Bash (only tested in bash, but should work in other terminals)
* cURL (switched to native python requests)

Payload Compatibility
------------
* Chrome (2018) - Tested live at Black Hat Arsenal 2017 and during extras development.
* Firefox - Untested - Should still work as available JS features are almost the same.

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
* Hello_Shell: Contains a Joomla extension backdoor, which can be uploaded as an administrator and 
               subsequently used to execute arbitrary commands on the system with ?c=ls or ?c64=base64_here.
               This directory was originally placed in "Joomla_Backdoor".
* Payloads/javascript: Contains the JavaScript payloads.
* Received_Data: Empty directory which will be used in future versions.
* Shells: Contains the PHP shells, including a slightly modified version of pentestmonkey's shell that 
          connects back via wget to send the attacker a notification of success.

Developed By
------------
* Hans-Michael Varbaek
* VarBITS

Special Credits
------------
* MaXe / InterN0T
* Sense of Security (Versions 2.0 - 2.5)

Code Design
-----------
* It works! (Again!)
* Still spaghetti code, but now with almost complete `PEP8` and possible refactoring in the future.
* Just-In-Time for Black Hat Europe 2017
