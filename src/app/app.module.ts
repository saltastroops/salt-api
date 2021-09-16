import { APP_INITIALIZER, ErrorHandler, NgModule } from '@angular/core';
import { Router } from '@angular/router';
import { BrowserModule } from '@angular/platform-browser';
import * as Sentry from '@sentry/angular';
import { DateFnsModule } from 'ngx-date-fns';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { HomeComponent } from './home/home.component';
import { ProposalComponent } from './proposal/proposal.component';
import { InvestigatorsComponent } from './proposal/investigators/investigators.component';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { HTTP_INTERCEPTORS, HttpClientModule } from '@angular/common/http';
import { ProposalService } from './service/proposal.service';
import { RealProposalService } from './service/real/real-proposal.service';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { nl2brPipe } from './nl2br.pipe';
import { LoadingSpinnerComponent } from './shared/loading-spinner/loading-spinner.component';
import { BlockService } from './service/block.service';
import { TooltipModule } from 'ng2-tooltip-directive';
import { RssSpectroscopyComponent } from './proposal/instruments/rss/rss-spectroscopy/rss-spectroscopy.component';
import { RssSlitMaskComponent } from './proposal/instruments/rss/rss-slit-mask/rss-slit-mask.component';
import { ArcBibleComponent } from './proposal/instruments/rss/arc-bible/arc-bible.component';
import { RssGeneralInfoComponent } from './proposal/instruments/rss/rss-general-info/rss-general-info.component';
import { RssCalibrationComponent } from './proposal/instruments/rss/rss-calibration/rss-calibration.component';
import { MosSlitMaskComponent } from './proposal/instruments/rss/mos-slit-mask/mos-slit-mask.component';
import { PolarimetryComponent } from './proposal/instruments/rss/polarimetry/polarimetry.component';
import { PolarimetricImagingComponent } from './proposal/instruments/rss/polarimetric-imaging/polarimetric-imaging.component';
import { EtalonWavelengthsComponent } from './proposal/instruments/rss/etalon-wavelengths/etalon-wavelengths.component';
import { FabryPerotComponent } from './proposal/instruments/rss/fabry-perot/fabry-perot.component';
import { ObservationComponent } from './proposal/blocks/block/observation/observation.component';
import { PayloadConfigurationComponent } from './proposal/blocks/block/payload-configuration/payload-configuration.component';
import { SummaryOfExecutedObservationsComponent } from './proposal/general/summary-of-executed-observations/summary-of-executed-observations.component';
import { ProposalProgressTableComponent } from './proposal/general/proposal-progress-table/proposal-progress-table.component';
import { ChargedTimeComponent } from './proposal/general/charged-time/charged-time.component';
import { TimeAllocationTableComponent } from './proposal/general/time-allocation-table/time-allocation-table.component';
import { SalticamDetectorComponent } from './proposal/instruments/salticam/salticam-detector-table/salticam-detector.component';
import { RssComponent } from './proposal/instruments/rss/rss.component';
import { RssDetectorComponent } from './proposal/instruments/rss/rss-detector/rss-detector.component';
import { ObservingConditionsComponent } from './proposal/blocks/block/observing-conditions/observing-conditions.component';
import { IterationsComponent } from './proposal/blocks/block/iterations/iterations.component';
import { BlockComponent } from './proposal/blocks/block/block.component';
import { TotalObservationTimeComponent } from './proposal/blocks/block/total-observation-time/total-observation-time.component';
import { ObservingWindowsComponent } from './proposal/blocks/block/observing-windows/observing-windows.component';
import { PriorityCommentComponent } from './proposal/blocks/block/priority-comment/priority-comment.component';
import { HrsComponent } from './proposal/instruments/hrs/hrs.component';
import { HrsObservingTimesComponent } from './proposal/instruments/hrs/hrs-observing-times/hrs-observing-times.component';
import { TargetComponent } from './proposal/target/target.component';
import { BvitComponent } from './proposal/instruments/bvit/bvit.component';
import { SalticamComponent } from './proposal/instruments/salticam/salticam.component';
import { SalticamGeneralInfoComponent } from './proposal/instruments/salticam/salticam-general-info/salticam-general-info.component';
import { SalticamObservationTimesComponent } from './proposal/instruments/salticam/salticam-observation-times/salticam-observation-times.component';
import { SalticamFiltersComponent } from './proposal/instruments/salticam/salticam-filters/salticam-filters.component';
import { HrsGeneralInfoComponent } from './proposal/instruments/hrs/hrs-general-info/hrs-general-info.component';
import { HrsConfigurationComponent } from './proposal/instruments/hrs/hrs-configuration/hrs-configuration.component';
import { HrsDetectorComponent } from './proposal/instruments/hrs/hrs-detector/hrs-detector.component';
import { ObservationCommentsComponent } from './proposal/general/observation-comments/observation-comments.component';
import { ObservationProbabilitiesComponent } from './proposal/blocks/block/observation-probabilities/observation-probabilities.component';
import { GeneralProposalInfoComponent } from './proposal/general/general-proposal-info/general-proposal-info.component';
import { BlockSummariesComponent } from './proposal/blocks/block-summaries/block-summaries.component';
import { ProposalDetailsComponent } from './proposal/general/proposal-details/proposal-details.component';
import { BlockSelectionComponent } from './proposal/blocks/block-view/block-selection/block-selection.component';
import { BlockViewComponent } from './proposal/blocks/block-view/block-view.component';
import { LoginComponent } from './login/login.component';
import { AuthGuardService } from './service/auth-guard.service';
import { AuthenticationInterceptor } from './service/authentication.interceptor.service';
import { RealBlockService } from './service/real/real-block.service';
import { AuthenticationService } from './service/authentication.service';
import { RealAuthenticationService } from './service/real/real-authentication.service';

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
    ChargedTimeComponent,
    ObservationCommentsComponent,
    ProposalProgressTableComponent,
    RssSpectroscopyComponent,
    RssSlitMaskComponent,
    SalticamDetectorComponent,
    ArcBibleComponent,
    ObservationComponent,
    RssComponent,
    RssGeneralInfoComponent,
    RssDetectorComponent,
    RssCalibrationComponent,
    RssComponent,
    ObservingConditionsComponent,
    IterationsComponent,
    BlockComponent,
    TotalObservationTimeComponent,
    ObservingWindowsComponent,
    ObservationProbabilitiesComponent,
    PriorityCommentComponent,
    ObservationComponent,
    PayloadConfigurationComponent,
    HrsComponent,
    HrsGeneralInfoComponent,
    HrsObservingTimesComponent,
    HrsConfigurationComponent,
    HrsDetectorComponent,
    TargetComponent,
    BvitComponent,
    MosSlitMaskComponent,
    SalticamComponent,
    SalticamGeneralInfoComponent,
    SalticamObservationTimesComponent,
    SalticamDetectorComponent,
    SalticamFiltersComponent,
    PolarimetryComponent,
    PolarimetricImagingComponent,
    EtalonWavelengthsComponent,
    FabryPerotComponent,
    LoginComponent,
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
    {
      provide: ErrorHandler,
      useValue: Sentry.createErrorHandler({ showDialog: true }),
    },
    { provide: Sentry.TraceService, deps: [Router] },
    {
      provide: APP_INITIALIZER,
      useFactory: () => () => {},
      deps: [Sentry.TraceService],
      multi: true,
    },
    { provide: ProposalService, useClass: RealProposalService },
    { provide: BlockService, useClass: RealBlockService },
    { provide: AuthenticationService, useClass: RealAuthenticationService },
    { provide: AuthGuardService, useClass: AuthGuardService },
    {
      provide: HTTP_INTERCEPTORS,
      useClass: AuthenticationInterceptor,
      multi: true,
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
