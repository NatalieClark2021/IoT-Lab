import time
from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import subprocess
import mysql.connector
import requests

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes




def conjoin(userSample,ip):
    ip = ip.replace(".",",")
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
    return part1+userSample


#database stuff=============================================================


def add_deviceSQL(device_id, name, ip, description, device_type):
    
    try:
        cnx= mysql.connector.connect(host='localhost', user='root',password='pass13', database='iotdatabase') 
        cursor = cnx.cursor()

        query = ("INSERT INTO devicest (DeviceID, DeviceName, DeviceIP, DeviceDescription, deviceType)"
        "VALUES (%s, %s, %s, %s, %s);")
        cursor.execute(query, (device_id, name, ip, description, device_type))
        cnx.commit()
        cursor.close()
        cnx.close()
        return "success SQL add"
    
    except:
        return "failure to add"


def get_devicesSQL():
    cnx = mysql.connector.connect(host='localhost', user='root',password='pass13', database='iotdatabase') 
    cursor = cnx.cursor(dictionary=True)
    query =("SELECT * FROM devicest;")
    cursor.execute(query)
    devices = cursor.fetchall()

    cursor.close()
    cnx.close()

    return {"devices": devices} 


#tester function not for production
def delALL():
    cnx = mysql.connector.connect(host='localhost', user='root',password='pass13', database='iotdatabase') 
    cursor = cnx.cursor()
    query =("DELETE FROM devicest;")
    cursor.execute(query)
    cnx.commit()
    cursor.close()
   
    cnx.close()

    return "deleted"

def delete_deviceSQL(device_id):

    try:
        cnx= mysql.connector.connect(host='localhost', user='root',password='pass13', database='iotdatabase') 
        cursor = cnx.cursor()

        #SQL
        query ="DELETE FROM devicest WHERE DeviceID = %s;"
        cursor.execute(query, (device_id,))
        cnx.commit()

        cursor.close()
        cnx.close()
        
        return "success"
    except:
        return "failure"

    
def device_by_id(device_id):

    cnx= mysql.connector.connect(host='localhost', user='root',password='pass13', database='iotdatabase') 
    cursor = cnx.cursor(dictionary=True) 

    select_query = "SELECT * FROM devicest WHERE DeviceID = %s;"
    cursor.execute(select_query, (device_id,))
    device = cursor.fetchone() 

    cursor.close()
    cnx.close()

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

@app.route('/deletedevice', methods=['POST']) #working
def deleteDevice():
    
    response = "failure"
    data = request.get_json()
    
    theID = data.get("id")

    if theID:
        response = "success"
        delete_deviceSQL(theID)
        return {"message":"Deleted Device"}, 200

    else:
        response = "error"
        return {"error":"Failed to find Device"}, 404
    
    
    

@app.route('/getdevice', methods=['GET'])
def get_devices():
    response = "failure"
    result = get_devicesSQL()

    devices = result["devices"]

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

    if device_list:
        return jsonify(device_list),200

    return {"error": "No devices found"},404
    
    
@app.route('/adddevice', methods=['POST'])
def addDevice():
    response = "failure"
    data = request.get_json()
    
    name = data.get("name")
    ip = data.get("IP")
    id = data.get("ID")
    desc = data.get("desc")
    dType = data.get("type")
    

    if name and ip and id and desc and dType:
        response = "success"
        add_deviceSQL(id, name, ip, desc, dType)
        return {"message":"Created Device"}, 201 

    else:
        response = "error"
        return {"error": "data error"}, 400 
     
   
def CLIInit(type):
    type = type.replace(".", ":")
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
    
def theFile(type):
    type = type.replace(":", ".")
    return "C:\\Users\\Natal\\OneDrive\\demo\\Documents\\WORKzone\\IOTLab-Virtualization\\backend\\userSketch\\build\\"+type+"\\userSketch.ino.bin"
    
    


@app.route('/data', methods=['POST'])
def receive_data():
    #Read JSON data
   
    data = request.get_json()
    
    id = data.get("deviceID")
    flash_code = data.get("flashCode")
    if flash_code and id:
        device = device_by_id(id)
        
        ip = device["DeviceIP"]
        dtype = device["deviceType"]
        
        command_args = CLIInit(dtype)
        tf = theFile(dtype)
    

        if(create_ino_file("userSketch", flash_code, command_args,tf,ip)):
            return {"message": "sketch successful and device updated"},200
        else:
            return {"message": "sketch unsuccessful and device updated"},200
        
        # Log if both values are present
    else:
        return {"error": "failure to reach device"}, 400
        #on error to compile return data not successful


test1 = "void setup() { Serial.begin(9600); pinMode(2, OUTPUT); Serial.println(1); } void loop() { digitalWrite(2, HIGH); Serial.println(1); delay(500); digitalWrite(2, LOW); Serial.println(0); delay(500); }"
 #Make this not upload just compile
 




def create_ino_file(file_name, content,cmd,tf,ip):

    
    print("made it to create ino")
    
    content = conjoin(content,ip)

    # os.makedirs(user_folder, exist_ok=True)
    
    if not file_name.endswith(".ino"):
        file_name += ".ino"

    try:
        
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
