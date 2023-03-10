import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule } from '@angular/common/http';
import { FormsModule } from '@angular/forms';


import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { NavbarComponent } from './dairy/dairy-navbar/navbar.component';
import { DairyHomeComponent } from './dairy/dairy-home/dairy-home.component';
import { DairyFooterComponent } from './dairy/dairy-footer/dairy-footer.component';
import { DairyCowListComponent } from './dairy/cow/dairy-cow-list/dairy-cow-list.component';
import { DairyCowCreateComponent } from './dairy/cow/dairy-cow-create/dairy-cow-create.component';
import { DairyCowUpdateComponent } from './dairy/cow/dairy-cow-update/dairy-cow-update.component';
import { DairyCowDetailComponent } from './dairy/cow/dairy-cow-detail/dairy-cow-detail.component';
import { DairyAboutUsComponent } from './dairy/dairy-about-us/dairy-about-us.component';
import { DairyContactUsComponent } from './dairy/dairy-contact-us/dairy-contact-us.component';

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
    DairyAboutUsComponent,
    DairyContactUsComponent,
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
