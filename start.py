# Code written by SayyadN
# Code Version 1.1.1
#Date : 5-6-2025
# Code For Download macOS Recovery and get macos (Images )

# Resources
#  macrecovery_open_core : https://tinyurl.com/bdfkbw43
#  olarila_vanilla_images: https://tinyurl.com/mr442fz6
#  olarila_efis : https://tinyurl.com/rkr3w93n

# Import Required Libraries
import os
import time
import webbrowser
import pyperclip


# Main variables for making programming easy
p = print
user_input = input
run = os.system
wait = time.sleep
ifit = os.path.exists
copy = pyperclip.copy
go = webbrowser.open



def check_files_path():
    macrecovery = ifit("macrecovery.py")
    macboards = ifit("boards.json")
    build_image = ifit("build-image.sh")
    
    check_list = []  # empty list for check files
    # checking file path if exists or not
    if macrecovery:
        check_list.append("macrecovery.py : Available")
    else:
        check_list.append("macrecovery.py : Not Available")
    if macboards:
        check_list.append("boards.json : Available")
    else:
        check_list.append("boards.json : Not Available")
    if build_image:
        check_list.append("build-image.sh : Available")
    else:
        check_list.append("build-image.sh : Not Available")

    p(check_list)
    
    # Stop the process if any file is not available
    if not (macrecovery and macboards and build_image):
        p("One or more required files are missing. Stopping the process.")
        exit(1)


def mac_recovery_download():
    # Lists of macos Recovery Downloads 
    macos_recovery_versions = [

        # Lion (10.7)
        {
            'version': '1 .Lion (10.7)',
            'commands': [
                'python3 macrecovery.py -b Mac-2E6FAB96566FE58C -m 00000000000F25Y00 download',
                'python3 macrecovery.py -b Mac-C3EC7CD22292981F -m 00000000000F0HM00 download'
            ]
        },
        
        # Mountain Lion (10.8)
        {
            'version': '2. Mountain Lion (10.8)',
            'commands': [
                'python3 macrecovery.py -b Mac-7DF2A3B5E5D671ED -m 00000000000F65100 download'
            ]
        },
        
        # Mavericks (10.9)
        {
            'version': '3. Mavericks (10.9)',
            'commands': [
                'python3 macrecovery.py -b Mac-F60DEB81FF30ACF6 -m 00000000000FNN100 download'
            ]
        },
        
        # Yosemite (10.10)
        {
            'version': '3. Yosemite (10.10)',
            'commands': [
                'python3 macrecovery.py -b Mac-E43C1C25D4880AD6 -m 00000000000GDVW00 download'
            ]
        },
        
        # El Capitan (10.11)
        {
            'version': '4. El Capitan (10.11)',
            'commands': [
                'python3 macrecovery.py -b Mac-FFE5EF870D7BA81A -m 00000000000GQRX00 download'
            ]
        },
        
        # Sierra (10.12)
        {
            'version': '5. Sierra (10.12)',
            'commands': [
                'python3 macrecovery.py -b Mac-77F17D7DA9285301 -m 00000000000J0DX00 download'
            ]
        },
        
        # High Sierra (10.13)
        {
            'version': '6. High Sierra (10.13)',
            'commands': [
                'python3 macrecovery.py -b Mac-7BA5B2D9E42DDD94 -m 00000000000J80300 download',
                'python3 macrecovery.py -b Mac-BE088AF8C5EB4FA2 -m 00000000000J80300 download'
            ]
        },
        
        # Mojave (10.14)
        {
            'version': '7. Mojave (10.14)',
            'commands': [
                'python3 macrecovery.py -b Mac-7BA5B2DFE22DDD8C -m 00000000000KXPG00 download'
            ]
        },
        
        # Catalina (10.15)
        {
            'version': '8. Catalina (10.15)',
            'commands': [
                'python3 macrecovery.py -b Mac-00BE6ED71E35EB86 -m 00000000000000000 download'
            ]
        },
        
        # Big Sur (11)
        {
            'version': '9. Big Sur (11)',
            'commands': [
                'python3 macrecovery.py -b Mac-42FD25EABCABB274 -m 00000000000000000 download'
            ]
        },
        
        # Monterey (12)
        {
            'version': '10. Monterey (12)',
            'commands': [
                'python3 macrecovery.py -b Mac-FFE5EF870D7BA81A -m 00000000000000000 download'
            ]
        },
        
        # Ventura (13)
        {
            'version': '11. Ventura (13)',
            'commands': [
                'python3 macrecovery.py -b Mac-4B682C642B45593E -m 00000000000000000 download'
            ]
        },
        
        # Sonoma (14)
        {
            'version': '12. Sonoma (14)',
            'commands': [
                'python3 macrecovery.py -b Mac-226CB3C6A851A671 -m 00000000000000000 download'
            ]
        },
        
        # Latest version - Sequoia (15)
        {
            'version': '13. Sequoia (Lasted)',
            'commands': [
                'python3 macrecovery.py -b Mac-937A206F2EE63C01 -m 00000000000000000 download'
            ]
        }
    ]
    
    # Checking Files Path
    check_files_path()

    p("This All Available macOS Recovery Versions:")
    wait(1)  # Wait One Second

    # For Command For Print all macos Recovery Available
    for mac in macos_recovery_versions:
        print(f"macOS Version: {mac['version']}")

    wait(.5)
     
    user_opion = int(user_input("Please Enter Your Number :" ))

    # IF Command For User Operations 
    if user_opion == 1:
        frist_ver = macos_recovery_versions[0]
        try:
            run(frist_ver['commands'][0])
        except:
            if len(frist_ver['commands']) > 1:
                run(frist_ver['commands'][1])
            else:
                p("Failed to run the command and no alternative command available.")
    elif user_opion == 2:
        second_ver = macos_recovery_versions[1]
        run(second_ver['commands'][0])
    elif user_opion == 3:
        third_ver = macos_recovery_versions[2]
        run(third_ver['commands'][0])
    elif user_opion == 4:
        forth_ver = macos_recovery_versions[3]
        run(forth_ver['commands'][0])
    elif user_opion == 5:
        fifth_ver = macos_recovery_versions[4]
        run(fifth_ver['commands'][0])
    elif user_opion == 6:
        sixth_ver = macos_recovery_versions[5]
        run(sixth_ver['commands'][0])
    elif user_opion == 7:
        seventh_ver = macos_recovery_versions[6]
        try:
            run(seventh_ver['commands'][0])
        except:
            if len(seventh_ver['commands']) > 1:
                run(seventh_ver['commands'][1])
            else:
                p("Failed to run the command and no alternative command available.")
    elif user_opion == 8:
        eighth_ver = macos_recovery_versions[7]
        run(eighth_ver['commands'][0])
    elif user_opion == 9:
        nineth_ver = macos_recovery_versions[8]
        run(nineth_ver['commands'][0])
    elif user_opion == 10:
        tenth_ver = macos_recovery_versions[9]
        run(tenth_ver['commands'][0])
    elif user_opion == 11:
        eleventh_ver = macos_recovery_versions[10]
        run(eleventh_ver['commands'][0])
    elif user_opion == 12:
        twelveth_ver = macos_recovery_versions[11]
        run(twelveth_ver['commands'][0])
    elif user_opion == 13:
        thirteenth_ver = macos_recovery_versions[12]
        run(thirteenth_ver['commands'][0])
    else:
        p("Invalid Option. Please try again.")
        exit(1)


def mac_os_download():
    # List Of macOS Images Versions Original 
    macos_images_versions = [
         # Lion (10.7)
        {
            'version': '1 .Lion (10.7)',
            'Link': [
                'https://tinyurl.com/lionmac'
            ]
        },
        
        # Mountain Lion (10.8)
        {
            'version': '2. Mountain Lion (10.8)',
            'Link': [
                'https://tinyurl.com/mlionosx'
            ]
        },
        
        # Mavericks (10.9)
        {
            'version': '3. Mavericks (10.9)',
            'Link': [
                'https://tinyurl.com/Mavericksx'
            ]
        },
        
        # Yosemite (10.10)
        {
            'version': '4. Yosemite (10.10)',
            'Link': [
                'https://tinyurl.com/Yosemitesx'
            ]
        },
        
        # El Capitan (10.11)
        {
            'version': '5. El Capitan (10.11)',
            'Link': [
                'https://tinyurl.com/capitanosx'
            ]
        },
        
        # Sierra (10.12)
        {
            'version': '6. Sierra (10.12)',
            'Link': [
                'https://tinyurl.com/sierramacx'
            ]
        },
        
        # High Sierra (10.13)
        {
            'version': '7. High Sierra (10.13)',
            'Link': [
                'https://tinyurl.com/machsierra'
            ]
        },
        
        # Mojave (10.14)
        {
            'version': '8. Mojave (10.14)',
            'Link': [
                'https://tinyurl.com/Mojaveosx'
            ]
        },
        
        # Catalina (10.15)
        {
            'version': '9. Catalina (10.15)',
            'Link': [
                'https://tinyurl.com/Catalinamacx'
            ]
        },
        
        # Big Sur (11)
        {
            'version': '10. Big Sur (11)',
            'Link': [
                'https://tinyurl.com/Bigsurosx'
            ]
        },
        
        # Monterey (12)
        {
            'version': '11. Monterey (12)',
            'Link': [
                'https://tinyurl.com/bdnhhbnm'
            ]
        },
        
        # Ventura (13)
        {
            'version': '12. Ventura (13)',
            'Link': [
                'https://tinyurl.com/2aaccm3s'
            ]
        },
        
        # Sonoma (14)
        {
            'version': '13. Sonoma (14)',
            'Link': [
                'https://tinyurl.com/mpwzvsmu'
            ]
        },
        # Latest version - Sequoia (15)
        {
            'version': '14. Sequoia (15)',
            'Link': [
                'https://tinyurl.com/2mwx8xf2'
                
            ]
        }
    ]
    # Print All macOS Images Versions
    for mac_img in macos_images_versions:
        print(f"macOS Version: {mac_img['version']}")

    wait(1)  # Wait One Second
    user_opion = int(user_input("Please Enter Your Number :" ))

    # Checking User Input And Run Command

    if user_opion == 1:
        frist_ver = macos_images_versions[0]
        copy(frist_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(frist_ver['Link'][0])
    elif user_opion == 2:
        second_ver = macos_images_versions[1]
        copy(second_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(second_ver['Link'][0])
    elif user_opion == 3:
        third_ver = macos_images_versions[2]
        copy(third_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(third_ver['Link'][0])
    elif user_opion == 4:
        forth_ver = macos_images_versions[3]
        copy(forth_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(forth_ver['Link'][0])
    elif user_opion == 5:
        fifth_ver = macos_images_versions[4]
        copy(fifth_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(fifth_ver['Link'][0])
    elif user_opion == 6:
        sixth_ver = macos_images_versions[5]
        copy(sixth_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(sixth_ver['Link'][0])
    elif user_opion == 7:
        seventh_ver = macos_images_versions[6]
        copy(seventh_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(seventh_ver['Link'][0])
    elif user_opion == 8:
        eighth_ver = macos_images_versions[7]
        copy(eighth_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(eighth_ver['Link'][0])
    elif user_opion == 9:
        nineth_ver = macos_images_versions[8]
        copy(nineth_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(nineth_ver['Link'][0])
    elif user_opion == 10:
        tenth_ver = macos_images_versions[9]
        copy(tenth_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(tenth_ver['Link'][0])
    elif user_opion == 11:
        eleventh_ver = macos_images_versions[10]
        copy(eleventh_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(eleventh_ver['Link'][0])
    elif user_opion == 12:
        twelveth_ver = macos_images_versions[11]
        copy(twelveth_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(twelveth_ver['Link'][0])
    elif user_opion == 13:
        thirteenth_ver = macos_images_versions[12]
        copy(thirteenth_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(thirteenth_ver['Link'][0])
    elif user_opion == 14:
        fourteenth_ver = macos_images_versions[13]
        copy(fourteenth_ver['Link'][0])
        p("Link Copied to Clipboard and Opened in Browser.")
        go(fourteenth_ver['Link'][0])
    else:
        p("Invalid Option. Please try again.")
        exit(1)


# main function 
def main():
    p("App made by SayyadN")
    p("Welcome to macOS Recovery and macOS Image Download Tool.")
    p("Please choose one of the following options:")
    p("1. Download macOS Recovery")
    p("2. Download macOS Image")
    p("3. Check Files Path")
    p("4. Exit")
    wait(1)  # Wait One Second

    user_option = int(user_input("Please Enter Your Number :" ))

    # Checking User Input And Run Command
    if user_option == 1:
        mac_recovery_download()
    elif user_option == 2:
        mac_os_download()
    elif user_option == 3:
        check_files_path()
    elif user_option == 4:
        p("Exiting the program.")
        exit()
        return 0 
    else:
        p("Invalid Option. Please try again.")
        exit(1)


if __name__ == "__main__":
    main()
