import { NgModule, Pipe, PipeTransform } from '@angular/core';
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
import { SummaryOfExecutedObservationsComponent } from './proposal/summary-of-executed-observations/summary-of-executed-observations.component';
import { ProposalDetailsComponent } from './proposal/proposal-details/proposal-details.component';
import { nl2brPipe } from './nl2br.pipe';
import { LoadingSpinnerComponent } from './shared/loading-spinner/loading-spinner.component';
import { BlockService } from './service/block.service';
import { MockBlockService } from './mock/service/mock-block.service';

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
    ProposalDetailsComponent,
    nl2brPipe,
    LoadingSpinnerComponent,
    SummaryOfExecutedObservationsComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule
  ],
  providers: [
    { provide: ProposalService, useClass: RealProposalService },
    { provide: BlockService, useClass: MockBlockService },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
