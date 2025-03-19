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
  url = 'http://127.0.0.1:80';
  name = '';

  devices: any[] = [];

  // Form controls
  selectedDevice = new FormControl('');


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

  ngOnInit(): void {
      this.pullDevices();
  }

  pullDevices(){
    this.http.get<any>(`${this.url}/getdevice`).subscribe(data => {
      this.devices = data;
      this.selectedDevice.setValue(this.devices[0].id);
      console.log("done");
    })
  }

 sendForm(){
    var myData = {
      deviceID: this.selectedDevice.value ,
      flashCode: this.flashCode.value
    };
    var termVal = document.getElementById("terminalValue");

    if(termVal){
      termVal.innerText = "Loading..."
    }

    this.http.post(`${this.url}/data`, myData).subscribe(data =>{
      console.log("done" + data);

      if(termVal){
        termVal.innerText = data + " - server"
      }
  
    })
  } 
  
 //http


   //http get request to server
}

