import { Component } from '@angular/core';
import { FormControl , FormGroup, FormsModule, ReactiveFormsModule} from '@angular/forms';
import { CommonModule } from '@angular/common'; 
import { HttpClient } from '@angular/common/http';
@Component({
  selector: 'app-admin',
  standalone: true,
  imports: [ReactiveFormsModule, FormsModule,CommonModule],
  templateUrl: './admin.component.html',
  styleUrl: './admin.component.css'
})
export class AdminComponent {


  constructor(private http: HttpClient){}

  url = 'http://127.0.0.1:80';

  newDev = new FormGroup ({
    IP: new FormControl(''),
    ID: new FormControl(''),
    desc: new FormControl(''),
    name: new FormControl(''),
    type: new FormControl('')
  });


  ID =  new FormControl('');
  selectedValue = '';





  addDevice(){
    var theData = this.newDev.value;

    this.http.post(`${this.url}/adddevice`, theData).subscribe(data =>{
      var termVal = document.getElementById("response");
    
      if(termVal){
        termVal.innerText = "Response from server: " + data;
      }
    })


  }
  
  
  deleteDevice(){
    var theData = {
      id: this.ID.value};

      this.http.post(`${this.url}/deletedevice`, theData).subscribe(data =>{
        var termVal = document.getElementById("response");
        if(termVal){
          termVal.innerText = "Response from server: " + data;
        }
      })

  }



}
