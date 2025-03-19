
import { RouterModule,Routes } from '@angular/router';
import { HomeComponent } from './home/home.component';
import { FlashComponent } from './flash/flash.component';
import { AdminComponent } from './admin/admin.component';



const routes: Routes = [
    {path: '',  component: HomeComponent, title: "home"},
    {path: 'flash', component: FlashComponent},
    {path: 'admin', component: AdminComponent},
    {path: 'home', component: HomeComponent}
];


export default routes;

