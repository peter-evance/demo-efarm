import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';

import { NavbarComponent } from './dairy/components/navbar/navbar.component';
import { DairyHomeComponent } from './dairy/components/dairy-home/dairy-home.component';
import { DairyFooterComponent } from './dairy/components/dairy-footer/dairy-footer.component';
import { DairyCowListComponent } from './dairy/components/cow/dairy-cow-list/dairy-cow-list.component';
import { DairyCowCreateComponent } from './dairy/components/cow/dairy-cow-create/dairy-cow-create.component';
import { DairyCowUpdateComponent } from './dairy/components/cow/dairy-cow-update/dairy-cow-update.component';
import { DairyCowDetailComponent } from './dairy/components/cow/dairy-cow-detail/dairy-cow-detail.component';
import { DairyMilkCreateComponent } from './dairy/components/milk/dairy-milk-create/dairy-milk-create.component';
import { DairyMilkListComponent } from './dairy/components/milk/dairy-milk-list/dairy-milk-list.component';
import { DairyMilkDetailComponent } from './dairy/components/milk/dairy-milk-detail/dairy-milk-detail.component';
import { DairyMilkUpdateComponent } from './dairy/components/milk/dairy-milk-update/dairy-milk-update.component';
import { DairyAboutUsComponent } from './dairy/components/dairy-about-us/dairy-about-us.component';
import { DairyContactUsComponent } from './dairy/components/dairy-contact-us/dairy-contact-us.component';
import { DairyPregnancyCreateComponent } from './dairy/components/pregnancy/dairy-pregnancy-create/dairy-pregnancy-create.component';
import { DairyPregnancyDetailComponent } from './dairy/components/pregnancy/dairy-pregnancy-detail/dairy-pregnancy-detail.component';
import { DairyPregnancyUpdateComponent } from './dairy/components/pregnancy/dairy-pregnancy-update/dairy-pregnancy-update.component';
import { DairyPregnancyListComponent } from './dairy/components/pregnancy/dairy-pregnancy-list/dairy-pregnancy-list.component';
import { DairyLactationListComponent } from './dairy/components/lactation/dairy-lactation-list/dairy-lactation-list.component';
import { MilkProductionComponent } from './dairy/components/admin/dashboard/milk/milk-production/milk-production.component';
import { MilkedCowsTodayComponent } from './dairy/components/admin/dashboard/milk/milked-cows-today/milked-cows-today.component';
import { DairyDashboardComponent } from './dairy/components/admin/dashboard/dairy-dashboard/dairy-dashboard.component';
import { MilkProductionWeeklyChartComponent } from './dairy/components/admin/analytics/milk/charts/milk-production-weekly-chart/milk-production-weekly-chart.component';
import { MilkProductionMonthlyComponent } from './dairy/components/admin/dashboard/milk/milk-production-monthly/milk-production-monthly.component';
import { TotalAliveCowsComponent } from './dairy/components/admin/dashboard/cows/total-alive-cows/total-alive-cows.component';
import { TotalAliveFemaleCowsComponent } from './dairy/components/admin/dashboard/cows/total-alive-female-cows/total-alive-female-cows.component';
import { TotalAliveMaleCowsComponent } from './dairy/components/admin/dashboard/cows/total-alive-male-cows/total-alive-male-cows.component';
import { TotalPregnantCowsComponent } from './dairy/components/admin/dashboard/cows/total-pregnant-cows/total-pregnant-cows.component';
import { TotalLactatingCowsComponent } from './dairy/components/admin/dashboard/cows/total-lactating-cows/total-lactating-cows.component';
import { LillyComponent } from './dairy/lilly/lilly.component';

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
    LillyComponent,
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
