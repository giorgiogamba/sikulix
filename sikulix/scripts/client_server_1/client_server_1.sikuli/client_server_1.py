# Testing connection script

# Script setup

## Server screen setup
server_screen = Screen(0) # set default screen
found_server = False

for i in range(Screen.getNumberScreens()):
    screen = Screen(i)
    if screen.exists("1759399839694.png"):
        found_server = True
        server_screen = screen
        print("found server screen")
        break

if not found_server:
    print("unable to find server. Exit...")
    quit()

# Client screen setup    
client_screen = Screen(0) # set default screen
found_client = False

for i in range(Screen.getNumberScreens()):
    screen = Screen(i)
    if screen.exists("1759400120767.png"):
        found_client = True
        client_screen = screen
        print("found client screen")
        break

if not found_client:
    print("unable to find client. Exit...")
    quit()

# Server start
server_screen.click("1759398479349.png")
server_screen.wait("1759398529789.png")

## Client connection
client_screen.click("1759398719570.png")
client_screen.wait("1759398593383.png")

# Command launch
client_screen.click("1759400416557.png")
server_screen.wait("1759400442376.png")

client_screen.click("1759400536979.png")
server_screen.wait("1759400582463.png")
client_screen.click("1759400546909.png")
server_screen.wait("1759400593095.png")
client_screen.click("1759400556207.png")
server_screen.wait("1759400604024.png")
client_screen.click("1759400565977.png")
server_screen.wait("1759400616376.png")

quit()








