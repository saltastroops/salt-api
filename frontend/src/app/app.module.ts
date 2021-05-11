import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { ProposalComponent } from './proposal/proposal.component';
import { InvestigatorsComponent } from './proposal/investigators/investigators.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ProposalComponent,
    InvestigatorsComponent
  ],
  imports: [
    BrowserModule,
    AppRoutingModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
