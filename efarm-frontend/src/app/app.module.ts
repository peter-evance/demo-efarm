import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './dairy/navbar/navbar.component';
import { DairyHomeComponent } from './dairy/dairy-home/dairy-home.component';
import { DairyFooterComponent } from './dairy/dairy-footer/dairy-footer.component';
import { DairyCowListComponent } from './dairy/cow/dairy-cow-list/dairy-cow-list.component';
import { DairyCowCreateComponent } from './dairy/cow/dairy-cow-create/dairy-cow-create.component';
import { DairyCowUpdateComponent } from './dairy/cow/dairy-cow-update/dairy-cow-update.component';
import { DairyCowDetailComponent } from './dairy/cow/dairy-cow-detail/dairy-cow-detail.component';
import { DairyMilkCreateComponent } from './dairy/milk/dairy-milk-create/dairy-milk-create.component';
import { DairyMilkListComponent } from './dairy/milk/dairy-milk-list/dairy-milk-list.component';
import { DairyMilkDetailComponent } from './dairy/milk/dairy-milk-detail/dairy-milk-detail.component';
import { DairyMilkUpdateComponent } from './dairy/milk/dairy-milk-update/dairy-milk-update.component';
import { DairyAboutUsComponent } from './dairy/dairy-about-us/dairy-about-us.component';
import { DairyContactUsComponent } from './dairy/dairy-contact-us/dairy-contact-us.component';
import { DairyPregnancyCreateComponent } from './dairy/pregnancy/dairy-pregnancy-create/dairy-pregnancy-create.component';
import { DairyPregnancyDetailComponent } from './dairy/pregnancy/dairy-pregnancy-detail/dairy-pregnancy-detail.component';
import { DairyPregnancyUpdateComponent } from './dairy/pregnancy/dairy-pregnancy-update/dairy-pregnancy-update.component';
import { DairyPregnancyListComponent } from './dairy/pregnancy/dairy-pregnancy-list/dairy-pregnancy-list.component';
import { DairyLactationListComponent } from './dairy/lactation/dairy-lactation-list/dairy-lactation-list.component';
import { MilkProductionComponent } from './dairy/admin/dashboard/milk/milk-production/milk-production.component';
import { MilkedCowsTodayComponent } from './dairy/admin/dashboard/milk/milked-cows-today/milked-cows-today.component';
import { DairyDashboardComponent } from './dairy/admin/dashboard/dairy-dashboard/dairy-dashboard.component';
import { MilkProductionWeeklyChartComponent } from './dairy/admin/analytics/milk/charts/milk-production-weekly-chart/milk-production-weekly-chart.component';
import { MilkProductionMonthlyComponent } from './dairy/admin/dashboard/milk/milk-production-monthly/milk-production-monthly.component';
import { TotalAliveCowsComponent } from './dairy/admin/dashboard/cows/total-alive-cows/total-alive-cows.component';
import { TotalAliveFemaleCowsComponent } from './dairy/admin/dashboard/cows/total-alive-female-cows/total-alive-female-cows.component';
import { TotalAliveMaleCowsComponent } from './dairy/admin/dashboard/cows/total-alive-male-cows/total-alive-male-cows.component';
import { TotalPregnantCowsComponent } from './dairy/admin/dashboard/cows/total-pregnant-cows/total-pregnant-cows.component';
import { TotalLactatingCowsComponent } from './dairy/admin/dashboard/cows/total-lactating-cows/total-lactating-cows.component';

@NgModule({
  declarations: [
    AppComponent,
    NavbarComponent,
    DairyHomeComponent,
    DairyFooterComponent,
    DairyCowListComponent,
    DairyCowCreateComponent,
    DairyCowUpdateComponent,
    DairyCowDetailComponent,
    DairyMilkCreateComponent,
    DairyMilkListComponent,
    DairyMilkDetailComponent,
    DairyMilkUpdateComponent,
    DairyAboutUsComponent,
    DairyContactUsComponent,
    DairyPregnancyCreateComponent,
    DairyPregnancyDetailComponent,
    DairyPregnancyUpdateComponent,
    DairyPregnancyListComponent,
    DairyLactationListComponent,
    MilkProductionComponent,
    MilkedCowsTodayComponent,
    DairyDashboardComponent,
    MilkProductionWeeklyChartComponent,
    MilkProductionMonthlyComponent,
    TotalAliveCowsComponent,
    TotalAliveFemaleCowsComponent,
    TotalAliveMaleCowsComponent,
    TotalPregnantCowsComponent,
    TotalLactatingCowsComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    FormsModule,
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
