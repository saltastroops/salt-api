import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { MatSliderModule } from '@angular/material/slider';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { ProposalComponent } from './proposal/proposal.component';
import { InvestigatorsComponent } from './proposal/investigators/investigators.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatButtonModule } from '@angular/material/button';
import { MatIconModule } from '@angular/material/icon';
import { HttpClientModule } from '@angular/common/http';
import { MatFormFieldModule, MatLabel } from '@angular/material/form-field';
import { MatSelectModule } from '@angular/material/select';
import { ProposalService } from './service/proposal.service';
import { RealProposalService } from './service/real/real-proposal.service';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { GeneralProposalInfoComponent } from './proposal/general-proposal-info/general-proposal-info.component';
import { BlockSummariesComponent } from './proposal/block-summaries/block-summaries.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ProposalComponent,
    InvestigatorsComponent,
    GeneralProposalInfoComponent,
    BlockSummariesComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    MatSliderModule,
    MatButtonModule,
    MatIconModule,
    MatFormFieldModule,
    MatSelectModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  providers: [{ provide: ProposalService, useClass: RealProposalService }],
  bootstrap: [AppComponent],
})
export class AppModule {}
