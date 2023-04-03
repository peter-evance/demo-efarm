import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { DairyCowCreateComponent } from './dairy/components/cow/dairy-cow-create/dairy-cow-create.component';
import { DairyCowDetailComponent } from './dairy/components/cow/dairy-cow-detail/dairy-cow-detail.component';
import { DairyCowListComponent } from './dairy/components/cow/dairy-cow-list/dairy-cow-list.component';
import { DairyCowUpdateComponent } from './dairy/components/cow/dairy-cow-update/dairy-cow-update.component';
import { DairyAboutUsComponent } from './dairy/components/dairy-about-us/dairy-about-us.component';
import { DairyContactUsComponent } from './dairy/components/dairy-contact-us/dairy-contact-us.component';
import { DairyHomeComponent } from './dairy/components/dairy-home/dairy-home.component';
import { DairyPregnancyListComponent} from './dairy/components/pregnancy/dairy-pregnancy-list/dairy-pregnancy-list.component';
import { DairyPregnancyCreateComponent} from './dairy/components/pregnancy/dairy-pregnancy-create/dairy-pregnancy-create.component';
import { DairyPregnancyDetailComponent} from './dairy/components/pregnancy/dairy-pregnancy-detail/dairy-pregnancy-detail.component';
import { DairyPregnancyUpdateComponent} from './dairy/components/pregnancy/dairy-pregnancy-update/dairy-pregnancy-update.component';
import { DairyLactationListComponent } from './dairy/components/lactation/dairy-lactation-list/dairy-lactation-list.component';
import { DairyMilkDetailComponent } from './dairy/components/milk/dairy-milk-detail/dairy-milk-detail.component';
import { DairyMilkListComponent } from './dairy/components/milk/dairy-milk-list/dairy-milk-list.component';
import { DairyMilkUpdateComponent } from './dairy/components/milk/dairy-milk-update/dairy-milk-update.component';
import { DairyMilkCreateComponent } from './dairy/components/milk/dairy-milk-create/dairy-milk-create.component';
import { DairyDashboardComponent } from './dairy/components/admin/dashboard/dairy-dashboard/dairy-dashboard.component';
import { TotalLactatingCowsComponent } from './dairy/components/admin/dashboard/cows/total-lactating-cows/total-lactating-cows.component';
import { TotalPregnantCowsComponent } from './dairy/components/admin/dashboard/cows/total-pregnant-cows/total-pregnant-cows.component';
import { MilkedCowsTodayComponent } from './dairy/components/admin/dashboard/milk/milked-cows-today/milked-cows-today.component';
import { MilkProductionComponent } from './dairy/components/admin/dashboard/milk/milk-production/milk-production.component';


const routes: Routes = [
  { path: 'dairy/home', component: DairyHomeComponent },
  { path: 'dairy/about-us', component: DairyAboutUsComponent },
  { path: 'dairy/contact-us', component: DairyContactUsComponent },
  { path: 'dairy/cows', component: DairyCowListComponent },
  { path: 'dairy/cows/create', component: DairyCowCreateComponent },
  { path: 'dairy/cows/update/:id', component: DairyCowUpdateComponent}, // pathMatch: 'full', data: { title: 'Update Cow' } },
  { path: 'dairy/cows/:id', component: DairyCowDetailComponent },
  { path: 'dairy/pregnancies', component: DairyPregnancyListComponent},
  { path: 'dairy/pregnancies/add', component: DairyPregnancyCreateComponent},
  { path: 'dairy/pregnancies/update/:id', component: DairyPregnancyDetailComponent},
  { path: 'dairy/pregnancies/:id', component: DairyPregnancyUpdateComponent},
  { path: 'dairy/lactations', component:DairyLactationListComponent},
  { path: 'dairy/milk/add', component: DairyMilkCreateComponent},
  { path: 'dairy/milk/update/:id', component: DairyMilkUpdateComponent},
  { path: 'dairy/milk/:id', component: DairyMilkDetailComponent},
  { path: 'dairy/milk', component: DairyMilkListComponent},

  // Admin routes
  { path: 'dairy/admin/dashboard', component: DairyDashboardComponent},
  { path: 'dairy/admin/dashboard', component: MilkProductionComponent},
  { path: 'dairy/admin/dashboard', component: MilkedCowsTodayComponent},
  { path: 'dairy/admin/dashboard', component: TotalPregnantCowsComponent},
  { path: 'dairy/admin/dashboard', component: TotalLactatingCowsComponent},];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
