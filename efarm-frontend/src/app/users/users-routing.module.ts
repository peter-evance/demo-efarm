import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { RegistrationComponent } from './components/registration/registration.component'; // Import the RegistrationComponent
import { LoginComponent } from './components/login/login.component';
import { LogoutComponent } from './components/logout/logout.component';
import { logOutGuard, loginGuard, registrationGuard } from '../shared/auth.guard';

const routes: Routes = [
  { path: 'register', component: RegistrationComponent,canActivate: [registrationGuard], data: { routeName: 'register' } },
  { path: 'login', component: LoginComponent, canActivate: [loginGuard], data: { routeName: 'login' } },
  { path: 'logout', component: LogoutComponent, canActivate: [logOutGuard], data: { routeName: 'logout' } },
];

@NgModule({
  imports: [RouterModule.forChild(routes)],
  exports: [RouterModule]
})
export class UsersRoutingModule { }
