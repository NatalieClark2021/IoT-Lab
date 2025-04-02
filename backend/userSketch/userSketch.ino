
    
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
        IPAddress LocalIP(192,168,1,22);
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
        void setup() {

    //setup initializer
    Serial.begin(115200);
    staMode();
    webServerInit();
    tkSecond.attach(1, everySecond);

     // Your setup code here
    pinMode(2,OUTPUT);
  
  }
  

void loop() {

    //loop initializer
    server.handleClient();
    delay(10);
    
    // Your loop code here
    digitalWrite(2,HIGH);
    delay(500);
    digitalWrite(2,LOW);
    delay(500);

  }