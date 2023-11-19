import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { UsersModule } from './users/users.module';

const routes: Routes = [
];


@NgModule({
  imports: [RouterModule.forRoot(routes), UsersModule],
  exports: [RouterModule]
})
export class AppRoutingModule { }
