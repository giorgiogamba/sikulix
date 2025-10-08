# Activate OCR feature
import org.sikuli.basics.Settings as Settings
Settings.OcrTextRead = True
Settings.OcrTextSearch = True

## Server screen setup
server_screen = Screen(0) # set default screen
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
client_screen = Screen(0) # set default screen
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

# #TEST: Put both applications in the top-left part of the screens,
# in order to test the sikulix's Region search
server_region = Region(server_screen.x, server_screen.y, 600, 600)
server_region.highlight(1)

client_region = Region(client_screen.x, client_screen.y, 600, 600)
client_region.highlight(1)

# OCR feature test
start_server_img = "1759398479349.png"
img_path = os.path.join(getBundlePath(), start_server_img)

try:
    # Direct Tesseract invokation for OCR
    process = subprocess.Popen(
        ['tesseract', img_path, 'stdout'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    output, error = process.communicate()
    text = output.strip()
    print("OCR Result:", text)
except Exception as e:
    print("OCR Error:", e)

# Server start
server_region.click("1759398479349.png")
server_region.wait("1759398529789.png")

## Client connection
client_region.click("1759398719570.png")
client_region.wait("1759398593383.png")

# Command launch
client_region.click("1759400416557.png")
server_region.wait("1759400442376.png")
client_region.click("1759400536979.png")
server_region.wait("1759400582463.png")
client_region.click("1759400546909.png")
server_region.wait("1759400593095.png")