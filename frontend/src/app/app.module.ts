import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { DateFnsModule } from 'ngx-date-fns';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { ProposalComponent } from './proposal/proposal.component';
import { InvestigatorsComponent } from './proposal/investigators/investigators.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HttpClientModule } from '@angular/common/http';
import { ProposalService } from './service/proposal.service';
import { RealProposalService } from './service/real/real-proposal.service';
import { TimeAllocationTableComponent } from './proposal/time-allocation-table/time-allocation-table.component';
import { ChargedTimeTableComponent } from './proposal/charged-time-table/charged-time-table.component';
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
import { TooltipModule } from 'ng2-tooltip-directive';
import { ProposalCommentsComponent } from './proposal/proposal-comments/proposal-comments.component';
import { ProposalProgressTableComponent } from './proposal/proposal-progress-table/proposal-progress-table.component';

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
    TimeAllocationTableComponent,
    ChargedTimeTableComponent,
    ProposalCommentsComponent,
    ProposalProgressTableComponent,
  ],
  imports: [
    BrowserModule,
    AppRoutingModule,
    BrowserAnimationsModule,
    HttpClientModule,
    FormsModule,
    ReactiveFormsModule,
    TooltipModule,
    DateFnsModule.forRoot(),
  ],
  providers: [
    { provide: ProposalService, useClass: RealProposalService },
    { provide: BlockService, useClass: MockBlockService },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
