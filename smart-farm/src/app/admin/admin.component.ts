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
// our servers ip
  url = 'http://127.0.0.1:80';

  //initalizes the form group for adding devices
  newDev = new FormGroup ({
    IP: new FormControl(''),
    ID: new FormControl(''),
    desc: new FormControl(''),
    name: new FormControl(''),
    type: new FormControl('')
  });

// intializes the form controles for device ID
  ID =  new FormControl('');

  selectedValue = '';




//this is called on submitting the add device form
  addDevice(){
    // the data is set to all the values inputted with the form group
    var theData = this.newDev.value;

    //a post request is sent to the /addevice endpoint with the formgroup data
    this.http.post(`${this.url}/adddevice`, theData).subscribe(data =>{

      // a paragraph on the page shows the server response for easy development
      var termVal = document.getElementById("response");
  
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
  
  // the delete device function is called when the delete form is submitted
  deleteDevice(){
    //the data is labeled as id and set the the form control value
    var theData = {
      id: this.ID.value};

      // we send a post request to the /deletedevice endpoint along with the form data
      this.http.post(`${this.url}/deletedevice`, theData).subscribe(data =>{
 

        // the paragraph on the page updates with the servers response
        var termVal = document.getElementById("response");
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
