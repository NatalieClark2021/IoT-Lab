# IOTLab-Virtualization

This project allows any user to type code into our ide and remotely update devices. It serves to virtualize SEMO's IoT Lab to further research and provide a good tool for professors and students. 
Any student or faculty who wants further clarification on the project can reach me at NatalieClark2021@gmail.com
 
Steps to setup the front-end
1. npm install -g @angular/cli
2. download the project and cd into smart-farm
3. in the terminal run 'npm install'
4. run 'ng serve' to see the front end locally

Steps to setup the backend
1. download the project, and cd into the backend
2. option: make an environment to seperate the dependencies
3. make sure a new verson of python and pip are available using 'python -v' and 'pip --version'
4. in the terminal run the following pip commands to get all of the dependencies
    1. pip install flask
    2. pip install Flask-Cors
    3. pip install requests
    4. pip install mysql.connector
  
5. Go to the Arduino docs and donwload the CLI tool https://docs.arduino.cc/arduino-cli/installation/
6. These should cover the dependencies, if not, they are listed as imports at the top and should be simple to include
7. To run the server, in the terminal, run 'python serverSide.py'
8. Option: set up testing with Pytest
9. in the terminal run 'pip install -U pytest'
10. to run the tests in the terminal run 'pytest sample_test.py'

Steps to setup database
1. Download MySQL workbench for the database
2. Set up a host
3. Create the table with this line
    'CREATE TABLE devices ( DeviceID INT PRIMARY KEY, DeviceName VARCHAR(255), DeviceIP VARCHAR(255), DeviceDescription VARCHAR(255), created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP );'
4. input the information into the table

Steps to setup network
1. Acquire a wireless router.
2. Depending on what router you obtain you need to configure the router by following its set up guide. For example, the router that was used in the prototype required first a wired lan connection in order to configure it.
3. In the configuration, set a static IP address for it based on the network that you are using. (ie 192.168.2.10 255.255.255.0).
4. Create an SSID that is easy to remember and take note of it.
5. Create a password for the SSID and take note of it. The password can be as secure as you want, but you should follow basic password standards.
6. You can test connectivity by pinging devices that are connected to the router. For
example, the one used for the prototype had a menu that would display what was connected to it and the IP address given to that device due to the router having DHCP on it for devices that do not have a static address. After getting the IP address of the connected wireless device, ping the device through the command prompt on the hardwired computer and you should get a confirmation ping.
7. After the router is set up, you can now access the router wireless if need be by connecting to the SSID and in a web browser putting in the IP address that you set up statically.
