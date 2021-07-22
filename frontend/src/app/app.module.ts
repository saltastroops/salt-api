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
import { SpectroscopyTableComponent } from './proposal/instruments/rss/spectroscopy-table/spectroscopy-table.component';
import { SlitMaskTableComponent } from './proposal/instruments/rss/slit-mask/slit-mask-table.component';
import { DetectorTableComponent } from './proposal/instruments/detector-table/detector-table.component';
import { ArcBibleTableComponent } from './proposal/instruments/rss/arc-bible-table/arc-bible-table.component';
import { UsedInTableComponent } from './proposal/instruments/used-in-table/used-in-table.component';
import { RssConfigurationViewComponent } from './proposal/instruments/rss/rss-cofiguration-view/rss-configuration-view.component';
import { RssGeneralTableComponent } from './proposal/instruments/rss/rss-general-table/rss-general-table.component';
import { RssCalibrationTableComponent } from './proposal/instruments/rss/rss-calibration-table/rss-calibration-table.component';
import { RssViewComponent } from './proposal/instruments/rss/rss-view/rss-view.component';
import { ObservingConditionsComponent } from './proposal/block/observing-conditions/observing-conditions.component';
import { IterationsComponent } from './proposal/block/iterations/iterations.component';
import { BlockComponent } from './proposal/block/block.component';
import { TotalObservationTimeComponent } from './proposal/block/total-obs-time/total-observation-time.component';
import { ObservingWindowsComponent } from './proposal/block/observing-windows/observing-windows.component';
import { ProbabilityTableComponent } from './proposal/block/probability-table/probability-table.component';
import { PriorityCommentComponent } from './proposal/block/priority-comment/priority-comment.component';
import { SalticamComponent } from './proposal/salticam/salticam.component';
import { GeneralComponent } from './proposal/salticam/general/general.component';
import { ObservationTimesComponent } from './proposal/salticam/observation-times/observation-times.component';
import { DetectorTableComponent } from './proposal/salticam/detector-table/detector-table.component';
import { FiltersTableComponent } from './proposal/salticam/filters-table/filters-table.component';
import { PolarimetryTableComponent } from './proposal/instruments/rss/polarimetry-table/polarimetry-table.component';
import { PolarimetricImagingTableComponent } from './proposal/instruments/rss/polarimetric-imaging-table/polarimetric-imaging-table.component';

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
    SpectroscopyTableComponent,
    SlitMaskTableComponent,
    DetectorTableComponent,
    ArcBibleTableComponent,
    UsedInTableComponent,
    RssConfigurationViewComponent,
    RssGeneralTableComponent,
    RssCalibrationTableComponent,
    RssViewComponent,
    ObservingConditionsComponent,
    IterationsComponent,
    BlockComponent,
    TotalObservationTimeComponent,
    ObservingWindowsComponent,
    ProbabilityTableComponent,
    PriorityCommentComponent,
    SalticamComponent,
    GeneralComponent,
    ObservationTimesComponent,
    DetectorTableComponent,
    FiltersTableComponent,
    PolarimetryTableComponent,
    PolarimetricImagingTableComponent,
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
