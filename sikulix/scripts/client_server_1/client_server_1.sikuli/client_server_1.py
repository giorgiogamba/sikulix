# Activate OCR feature
import subprocess
import os
import org.sikuli.basics.Settings as Settings
Settings.OcrTextRead = True
Settings.OcrTextSearch = True

# Looks for the client and server applications inside the screen and 
# keeps track of them

## Server screen
server_screen = Screen(0)
found_server = False

for i in range(Screen.getNumberScreens()):
    print("Server: analyze screen " + str(i))
    screen = Screen(i)
    if screen.exists("1759399839694.png"):
        found_server = True
        server_screen = screen
        print("found server screen")
        break

if not found_server:
    print("unable to find server. Exit...")
    exit()

# Client screen setup
client_screen = Screen(0)
found_client = False

for i in range(Screen.getNumberScreens()):
    print("Client: analyze screen " + str(i))
    screen = Screen(i)
    if screen.exists("1759400120767.png"):
        found_client = True
        client_screen = screen
        print("found client screen")
        break

if not found_client:
    print("unable to find client. Exit...")
    exit()

# #TEST: Put both applications on the top-left part of the screens,
# in order to test the sikulix's Region search
server_region = Region(server_screen.x, server_screen.y, 600, 600)
server_region.highlight(1)

client_region = Region(client_screen.x, client_screen.y, 600, 600)
client_region.highlight(1)

# OCR feature test 1
# Read the provided image's text
start_server_img = "1759398479349.png"
img_path = os.path.join(getBundlePath(), start_server_img)

server_text = ""

try:
    # Direct Tesseract invokation for OCR
    process = subprocess.Popen(['tesseract', img_path, 'stdout'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    server_text = output.strip()
except Exception as e:
    print("OCR Error:", e)
    exit()

if server_text == "":
    print("Unable to find text, returning...")
    exit()
else:
    print("OCR Result:", server_text)
    
# OCR feature test 2
# Search for the text read from the image inside server region
# NOTE: The search is not working when the button is in "Disabled" mode (the server is already running)
server_region_path = capture(server_region)
try:
    process = subprocess.Popen(['tesseract', server_region_path, 'stdout'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    region_text = output.strip()
    if server_text in region_text:
        print("Found text inside server region")
    else:
        print("Text not found. Region contains:", region_text)
        exit()
except Exception as e:
    print("OCR Error:", e)
    exit()

# TEST: Execute commands on client and check if working on server

# Server start
server_region.click("1759398479349.png")
server_region.wait("1759398529789.png")

## Client connection
client_region.click("1759398719570.png")
client_region.wait("1759398593383.png")

# Commands launch
client_region.click("1759400416557.png")
server_region.wait("1759400442376.png")
client_region.click("1759400536979.png")
server_region.wait("1759400582463.png")
client_region.click("1759400546909.png")
server_region.wait("1759400593095.png")