import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { ProposalComponent } from './proposal/proposal.component';
import { InvestigatorsComponent } from './proposal/investigators/investigators.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { ProposalService } from './service/proposal.service';
import { RealProposalService } from './service/real/real-proposal.service';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { GeneralProposalInfoComponent } from './proposal/general-proposal-info/general-proposal-info.component';
import { BlockSummariesComponent } from './proposal/block-summaries/block-summaries.component';
import { BlockViewComponent } from './proposal/block-view/block-view.component';
import { BlockSelectionComponent } from './proposal/block-view/block-selection/block-selection.component';

@NgModule({
  declarations: [
    AppComponent,
    HomeComponent,
    ProposalComponent,
    InvestigatorsComponent,
    GeneralProposalInfoComponent,
    BlockSummariesComponent,
    BlockViewComponent,
    BlockSelectionComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
  ],
  providers: [{ provide: ProposalService, useClass: RealProposalService }],
  bootstrap: [AppComponent],
})
export class AppModule {}
