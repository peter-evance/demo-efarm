import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DairyCowCreateComponent } from './dairy/cow/dairy-cow-create/dairy-cow-create.component';
import { DairyCowDetailComponent } from './dairy/cow/dairy-cow-detail/dairy-cow-detail.component';
import { DairyCowListComponent } from './dairy/cow/dairy-cow-list/dairy-cow-list.component';
import { DairyCowUpdateComponent } from './dairy/cow/dairy-cow-update/dairy-cow-update.component';
import { DairyAboutUsComponent } from './dairy/dairy-about-us/dairy-about-us.component';
import { DairyContactUsComponent } from './dairy/dairy-contact-us/dairy-contact-us.component';
import { DairyHomeComponent } from './dairy/dairy-home/dairy-home.component';

const routes: Routes = [
  { path: 'dairy/home', component: DairyHomeComponent },
  { path: 'dairy/about-us', component: DairyAboutUsComponent },
  { path: 'dairy/contact-us', component: DairyContactUsComponent },
  { path: 'dairy/cows', component: DairyCowListComponent },
  { path: 'dairy/cows/create', component: DairyCowCreateComponent },
  { path: 'dairy/cows/update/:id', component: DairyCowUpdateComponent, pathMatch: 'full', data: { title: 'Update Cow' } },
  { path: 'dairy/cows/:id', component: DairyCowDetailComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
