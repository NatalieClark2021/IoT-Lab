import { HttpClient } from '@angular/common/http';

import { Component } from '@angular/core';
import { NgModel } from '@angular/forms';
import { CommonModule } from '@angular/common'; 
import {FormControl, ReactiveFormsModule} from '@angular/forms';
import { get } from 'http';

@Component({
  selector: 'app-flash',
  standalone: true,
  imports: [ReactiveFormsModule, CommonModule],
  templateUrl: './flash.component.html',
  styleUrl: './flash.component.css'
})
export class FlashComponent {
  //this the our servers ip
  url = 'http://127.0.0.1:80';
  name = '';

  //intitalize an array of devices to empty
  devices: any[] = [];

  // Form controls
  selectedDevice = new FormControl('');
  //flash code's form control is given some starter code in order to help a user write functional code in our IDE
  flashCode = new FormControl(
    `void setup() {

    //setup initializer
    Serial.begin(115200);
    staMode();
    webServerInit();
    tkSecond.attach(1, everySecond);

     // Your setup code here
  
  }
  

void loop() {

    //loop initializer
    server.handleClient();
    delay(10);
    
    // Your loop code here

  }`);

  constructor(private http: HttpClient){}

  // on component being initialized call pull devices to populate the drop down list
  ngOnInit(): void {
      this.pullDevices();
  }

  // pull devices sents a get request to the server and stores the returned data in the local devices
  pullDevices(){
    this.http.get<any>(`${this.url}/getdevice`).subscribe(data => {
      this.devices = data;
      // automaticall selects the first device
      this.selectedDevice.setValue(this.devices[0].id);
      console.log("done");
    })
  }

// when the user has chosen a device, and written some code for it, they can send the form
 sendForm(){
  // myData packages up json data with the tags deviceID and flashcode being set to their respective values
    var myData = {
      deviceID: this.selectedDevice.value ,
      flashCode: this.flashCode.value
    };

    //while we await the servers response we set the terminal to say loading
    var termVal = document.getElementById("terminalValue");
    if(termVal){
      termVal.innerText = "Loading..."
    }

    // this makes a post request to the /data endpoint
    this.http.post(`${this.url}/data`, myData).subscribe(data =>{
      console.log("done" + data);

      //on a successful message response or an error response, we print that to the terminal
      if ('message' in data){
        if(termVal){
          termVal.innerText = "Response from server: " + data.message;
        }
      }else if('error' in data){
        if(termVal){
          termVal.innerText = "Response from server: " + data.error;
        }
      }
  
    })
  } 
  
}

