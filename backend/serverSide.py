import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import subprocess
import mysql.connector
import requests

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes


# conjoin takes the user code, and celans the device IP address, and uses string interpolation in order to
# produce code that runs on the users specified device along with our teams OTA stub

def conjoin(userSample,ip):
    
    ip = ip.replace(".",",")

    #OTA STUB
    part1 = """
    
        #include <WiFi.h>
        #include <WebServer.h>
        #include <Update.h>
        #include <Ticker.h>
        // Literal string
        const char *indexHtml = R"literal(
        <!DOCTYPE html>
        <body style='width:480px'>
            <h2>ESP Firmware Update</h2>
            <form method='POST' enctype='multipart/form-data' id='upload-form'>
            <input type='file' id='file' name='update'>
            <input type='submit' value='Update'>
            </form>
            <br>
            <div id='prg' style='width:0;color:white;text-align:center'>0%</div>
        </body>
        <script>
            var prg = document.getElementById('prg');
            var form = document.getElementById('upload-form');
            form.addEventListener('submit', el=>{
            prg.style.backgroundColor = 'blue';
            el.preventDefault();
            var data = new FormData(form);
            var req = new XMLHttpRequest();
            var fsize = document.getElementById('file').files[0].size;
            req.open('POST', '/update?size=' + fsize);
            req.upload.addEventListener('progress', p=>{
                let w = Math.round(p.loaded/p.total*100) + '%';
                if(p.lengthComputable){
                    prg.innerHTML = w;
                    prg.style.width = w;
                }
                if(w == '100%') prg.style.backgroundColor = 'black';
            });
            req.send(data);
            });
        </script>
        )literal";

        // Compressed gzip in C include file style
        // listing was created using `xxd -i favicon.ico.gz`








        WebServer server(80);
        Ticker tkSecond;
        uint8_t otaDone = 0;
        String ssid = "IoT Test";
        String password = "password12";
        IPAddress LocalIP("""+ip+""");
        IPAddress gateway(192,168,1,1);
        IPAddress subnet(255,255,255,0);
        void staMode() {
            WiFi.mode(WIFI_STA);
            WiFi.config(LocalIP, gateway,subnet);
            WiFi.begin(ssid,password);  // Connect to the last known WiFi credentials
           
            while (WiFi.status() != WL_CONNECTED) {
                delay(500);
            }

        
        }

        void handleUpdateEnd() {
            server.sendHeader("Connection", "close");
            if (Update.hasError()) {
                server.send(502, "text/plain", Update.errorString());
            } else {
                server.sendHeader("Refresh", "10");
                server.sendHeader("Location", "/");
                server.send(307);
                ESP.restart();
            }
        }

        void handleUpdate() {
            HTTPUpload &upload = server.upload();
            if (upload.status == UPLOAD_FILE_START) {
                if (!Update.begin(UPDATE_SIZE_UNKNOWN)) {
                    otaDone = 0;
                    Update.printError(Serial);
                }
            } else if (upload.status == UPLOAD_FILE_WRITE) {
                if (Update.write(upload.buf, upload.currentSize) != upload.currentSize) {
                    Update.printError(Serial);
                } else {
                    otaDone = 100 * Update.progress() / Update.size();
                }
            } else if (upload.status == UPLOAD_FILE_END) {
                if (Update.end(true)) {
                
                    otaDone = 0;
                }
            }
        }

        void webServerInit() {
            server.on(
                "/update", HTTP_POST,
                []() { handleUpdateEnd(); },
                []() { handleUpdate(); }
            );
            server.on("/favicon.ico", HTTP_GET, []() {
                server.sendHeader("Content-Encoding", "gzip");
            });
            server.onNotFound([]() {
                server.send(200, "text/html", indexHtml);
            });
            server.begin();
            
        }

        void everySecond() {
            if (otaDone > 1) {
            }
        }
        """
    #appends our dynamic stub to the users code sent from the front end
    return part1+userSample


#database stuff=============================================================

#this function takes in all of the device data as parameters and uses it to insert a new device into the database
def add_deviceSQL(device_id, name, ip, description, device_type):
    
    try:
        #attempts to connect to the database
        cnx= mysql.connector.connect(host='localhost', user='root',password='pass13', database='iotdatabase') 
        cursor = cnx.cursor()

        #this section inserts our passed arguments and the performs the query
        query = ("INSERT INTO devicest (DeviceID, DeviceName, DeviceIP, DeviceDescription, deviceType)"
        "VALUES (%s, %s, %s, %s, %s);")
        cursor.execute(query, (device_id, name, ip, description, device_type))
        cnx.commit()
        cursor.close()
        cnx.close()

        #returns a success message
        return "success SQL add"
    
    except:
        return "failure to add"


# get devices allows us to connect to the database and query for all of the devices within the database
def get_devicesSQL():
    #we establish our connection
    cnx = mysql.connector.connect(host='localhost', user='root',password='pass13', database='iotdatabase') 
    cursor = cnx.cursor(dictionary=True)

    # Our query is performed
    query =("SELECT * FROM devicest;")
    cursor.execute(query)
    devices = cursor.fetchall()

    cursor.close()
    cnx.close()
    #we return the dictionary devices that is holding all of the returned devices
    return {"devices": devices} 


#tester function not for production
# This serves our unit tests allowing us to clean up the database after tests
def delALL():
    cnx = mysql.connector.connect(host='localhost', user='root',password='pass13', database='iotdatabase') 
    cursor = cnx.cursor()
    query =("DELETE FROM devicest;")
    cursor.execute(query)
    cnx.commit()
    cursor.close()
   
    cnx.close()

    return "deleted"

#This allows a user to pass a devices ID in order to delete it from the database
def delete_deviceSQL(device_id):

    try:
        #we connect to the database
        cnx= mysql.connector.connect(host='localhost', user='root',password='pass13', database='iotdatabase') 
        cursor = cnx.cursor()

        #we run our query passing in the devices id
        query ="DELETE FROM devicest WHERE DeviceID = %s;"
        cursor.execute(query, (device_id,))
        cnx.commit()

        cursor.close()
        cnx.close()
        
        return "success"
    except:
        return "failure"


# This function allows a user to select a device by passing in its ID
def device_by_id(device_id):

    #connect to the database
    cnx= mysql.connector.connect(host='localhost', user='root',password='pass13', database='iotdatabase') 
    cursor = cnx.cursor(dictionary=True) 

    #write then exceute our query passing in the id
    select_query = "SELECT * FROM devicest WHERE DeviceID = %s;"
    cursor.execute(select_query, (device_id,))
    device = cursor.fetchone() 

    cursor.close()
    cnx.close()

    #if the device is found we return that device as an object, otherwise we return none
    if device:
        print (device)
        return device
    else:
        return None

#=============================================================================



#data type for reference

# class Device:
#     def __init__(self, id, name, ip, desc, datatype):
#         self.id = id
#         self.name = name
#         self.ip = ip
#         self.desc = desc
#         self.datatype = datatype
    





#http requests
#this sets a route with an end point /deletedevice that expects a POST request
@app.route('/deletedevice', methods=['POST']) 
def deleteDevice():
    
    #we initialize our response to failure
    response = "failure"

    #we get the data passed to the endpoint and find the ID by the tag id
    data = request.get_json()
    theID = data.get("id")

    #if we successfully get that data, we call the function to delete that device, then return a success message and code 200
    #otherwise, we return a failure response and the code 404 for not found
    if theID:
        response = "success"
        delete_deviceSQL(theID)
        return {"message":"Deleted Device"}, 200

    else:
        response = "error"
        return {"error":"Failed to find Device"}, 404
    
    
    
#sets the end point /getdevice that expects a GET request
@app.route('/getdevice', methods=['GET'])
def get_devices():
    response = "failure"

    #we collect the devices from our get devices sql function, then get the actual devices from the dictionary tag devices
    result = get_devicesSQL()
    devices = result["devices"]

    #loop through the devices as device, then store the individual attributes of the devices as device objects, and store them in device_list
    device_list = [
        {
            "name": device['DeviceName'],
            "id": device['DeviceID'],
            "type": device['deviceType'],
            "ip": device['DeviceIP'],
            "desc": device['DeviceDescription']
        } 
        for device in devices
        ]

    #if the device is isnt empty, we return that data and a 200 success code
    # otherwise we return an error message and a 404 code
    if device_list:
        return jsonify(device_list),200

    return {"error": "No devices found"},404
    

#we create the /adddevice input and it expects a POST request
@app.route('/adddevice', methods=['POST'])
def addDevice():
    response = "failure"
    #we get the data sent to the server
    data = request.get_json()
    
    #each tag from within the data is stored into the individual attributes of the device
    name = data.get("name")
    ip = data.get("IP")
    id = data.get("ID")
    desc = data.get("desc")
    dType = data.get("type")
    

    #when each attribute is found we call our SQL function to add a device and return a success message with a 201 code
    if name and ip and id and desc and dType:
        response = "success"
        add_deviceSQL(id, name, ip, desc, dType)
        return {"message":"Created Device"}, 201 
    #otherwise we return the error message and 400 code
    else:
        response = "error"
        return {"error": "data error"}, 400 
     
# Our CLI initializer takes in the device type and initializes our CLI arguments
def CLIInit(type):
    #we clean the device type in case of user error
    type = type.replace(".", ":")
    #we pass in the standard arguments, as well as the device type
    command_args = [
    "arduino-cli", 
    "compile", 
    "C:\\Users\\Natal\\OneDrive\\demo\\Documents\\WORKzone\\IOTLab-Virtualization\\backend\\userSketch", 
    "-b", 
    type, 
    "--build-property", 
    "build.boot=dio",
    "--export-binaries" 
    
    ]  
    return command_args 

# we set a local files attributes to match its device type
def theFile(type):
    #we clean our device to protect from user error
    type = type.replace(":", ".")
    #we return the file path with the correct device type
    return "C:\\Users\\Natal\\OneDrive\\demo\\Documents\\WORKzone\\IOTLab-Virtualization\\backend\\userSketch\\build\\"+type+"\\userSketch.ino.bin"
    
    

# set up the endpoint data that expects a POST request
@app.route('/data', methods=['POST'])
def receive_data():
    #Read JSON data
    data = request.get_json()
    
    #get ID and code information from the json tags
    id = data.get("deviceID")
    flash_code = data.get("flashCode")

    #if both are present, we proceed
    if flash_code and id:
        #call our sql function in order to get the device and setting the needed attributed to ip and dtype respectively
        device = device_by_id(id)
        
        ip = device["DeviceIP"]
        dtype = device["deviceType"]
        
        #running command args and setting up the file information by passing in the device type
        command_args = CLIInit(dtype)
        tf = theFile(dtype)
    
        #if we successfully create an ino file with the arguments flashcode, command_args, tf, and ip, return a success message
        if(create_ino_file("userSketch", flash_code, command_args,tf,ip)):
            return {"message": "sketch successful and device updated"},200
        #otherwise return an error message
        else:
            return {"message": "sketch unsuccessful and device updated"},200
        
      
    else:
        return {"error": "failure to reach device"}, 400
        #on error to compile return data not successful


test1 = "void setup() { Serial.begin(9600); pinMode(2, OUTPUT); Serial.println(1); } void loop() { digitalWrite(2, HIGH); Serial.println(1); delay(500); digitalWrite(2, LOW); Serial.println(0); delay(500); }"
 #Make this not upload just compile
 



#the create ino file passing in arguments to give it the file name, the code it needs to write, the command line arguments, the configured file, and the ip address of the device
def create_ino_file(file_name, content,cmd,tf,ip):

    
    print("made it to create ino")
    
    #calls conjoin to dynamically set up our stub
    content = conjoin(content,ip)

    # os.makedirs(user_folder, exist_ok=True)
    
    #check if we have the proper file type, and if not, append .ino to it
    if not file_name.endswith(".ino"):
        file_name += ".ino"

    try:
        #write the content to the file
        with open("C:\\Users\\Natal\\OneDrive\\demo\\Documents\\WORKzone\\IOTLab-Virtualization\\backend\\userSketch\\userSketch.ino", 'w') as ino_file:
            ino_file.write(content)
        
        if(subprocess.call(cmd) == 0):
            #return True
            #Code block to send compiled binary to deviceip/update using POST Method
            
            with open(tf, "rb") as file:
                
                files = {'file': file}
                url = "http://" + ip +"/update?size="+str(os.path.getsize(tf))
                requests.post(url, files=files)
            return True
        else:
            return False
        
        #after running we get the file locaiton and send an HTTP Post to the deviceIP/upload with the binary attached to it
        #This requires the length of the file as well as the file both gathered from the standard python file functions
    
    except Exception as e:
        print(f"Error: {e}")
    
#test area==================================
 
 
 
#===========================================
        
if __name__ == '__main__':

    app.run(port=80)
