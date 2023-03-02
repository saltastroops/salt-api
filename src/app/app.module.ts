import { HTTP_INTERCEPTORS, HttpClientModule } from "@angular/common/http";
import { APP_INITIALIZER, ErrorHandler, NgModule } from "@angular/core";
import { FormsModule, ReactiveFormsModule } from "@angular/forms";
import { BrowserModule } from "@angular/platform-browser";
import { BrowserAnimationsModule } from "@angular/platform-browser/animations";
import { Router } from "@angular/router";

import * as Sentry from "@sentry/angular";
import { TooltipModule } from "ng2-tooltip-directive";
import { CookieService } from "ngx-cookie-service";
import { DateFnsModule } from "ngx-date-fns";

import { AppRoutingModule } from "./app-routing.module";
import { AppComponent } from "./app.component";
import { HomeGuestComponent } from "./home/home-guest/home-guest.component";
import { HomeUserComponent } from "./home/home-user/home-user.component";
import { HomeComponent } from "./home/home.component";
import { ChangePasswordComponent } from "./login/change-password/change-password.component";
import { ForgotPasswordComponent } from "./login/forgot-password/forgot-password.component";
import { LoginComponent } from "./login/login.component";
import { ManageUserProfileComponent } from "./manage-user-profile/manage-user-profile.component";
import { MosLegendComponent } from "./mos/legend/mos-legend.component";
import { MosBlocksTableComponent } from "./mos/mos-blocks-table/mos-blocks-table.component";
import { MosMaskUpdateModalComponent } from "./mos/mos-blocks-table/mos-mask-update-modal/mos-mask-update-modal.component";
import { MosComponent } from "./mos/mos.component";
import { ObsoleteMasksComponent } from "./mos/obsolete-masks/obsolete-masks.component";
import { InlineLoginComponent } from "./navigation-bar/inline-login/inline-login.component";
import { NavigationBarComponent } from "./navigation-bar/navigation-bar.component";
import { nl2brPipe } from "./pipes/nl2br.pipe";
import { SortByArgsPipe } from "./pipes/sort-by-args.pipe";
import { BlockSummariesComponent } from "./proposal/blocks/block-summaries/block-summaries.component";
import { BlockSelectionComponent } from "./proposal/blocks/block-view/block-selection/block-selection.component";
import { BlockViewComponent } from "./proposal/blocks/block-view/block-view.component";
import { BlockComponent } from "./proposal/blocks/block/block.component";
import { EditBlockStatusModalComponent } from "./proposal/blocks/block/edit-block-status-modal/edit-block-status-modal.component";
import { IterationsComponent } from "./proposal/blocks/block/iterations/iterations.component";
import { ObservationProbabilitiesComponent } from "./proposal/blocks/block/observation-probabilities/observation-probabilities.component";
import { ObservingConditionsComponent } from "./proposal/blocks/block/observing-conditions/observing-conditions.component";
import { ObservingWindowsComponent } from "./proposal/blocks/block/observing-windows/observing-windows.component";
import { PayloadConfigurationComponent } from "./proposal/blocks/block/payload-configuration/payload-configuration.component";
import { TotalObservationTimeComponent } from "./proposal/blocks/block/total-observation-time/total-observation-time.component";
import { ChargedTimeComponent } from "./proposal/general/charged-time/charged-time.component";
import { EditBlockVisitStatusModalComponent } from "./proposal/general/edit-block-visit-status-modal/edit-block-visit-status-modal.component";
import { GeneralProposalInfoComponent } from "./proposal/general/general-proposal-info/general-proposal-info.component";
import { ObservationCommentsComponent } from "./proposal/general/observation-comments/observation-comments.component";
import { DetailsTableComponent } from "./proposal/general/proposal-details/details-table/details-table.component";
import { EditProprietaryPeriodModalComponent } from "./proposal/general/proposal-details/edit-proprietary-period-modal/edit-proprietary-period-modal.component";
import { ProposalDetailsComponent } from "./proposal/general/proposal-details/proposal-details.component";
import { ProposalDownloadComponent } from "./proposal/general/proposal-details/proposal-download/proposal-download.component";
import { ProposalSummaryComponent } from "./proposal/general/proposal-details/proposal-summary/proposal-summary.component";
import { ResponsibleAstronomerComponent } from "./proposal/general/proposal-details/responsible-astronomer/responsible-astronomer.component";
import { ProgressRequestFormComponent } from "./proposal/general/proposal-progress/progress-request-form/progress-request-form.component";
import { ProposalProgressComponent } from "./proposal/general/proposal-progress/proposal-progress.component";
import { RequestedObservingConditionsComponent } from "./proposal/general/proposal-progress/requested-observing-conditions/requested-observing-conditions.component";
import { SubmittedTimeRequestsComponent } from "./proposal/general/proposal-progress/submitted-time-requests/submitted-time-requests.component";
import { SummaryOfExecutedObservationsComponent } from "./proposal/general/summary-of-executed-observations/summary-of-executed-observations.component";
import { TimeAllocationsTableComponent } from "./proposal/general/time-allocations-table/time-allocations-table.component";
import { BvitComponent } from "./proposal/instruments/bvit/bvit.component";
import { HrsConfigurationComponent } from "./proposal/instruments/hrs/hrs-configuration/hrs-configuration.component";
import { HrsDetectorComponent } from "./proposal/instruments/hrs/hrs-detector/hrs-detector.component";
import { HrsGeneralInfoComponent } from "./proposal/instruments/hrs/hrs-general-info/hrs-general-info.component";
import { HrsObservingTimesComponent } from "./proposal/instruments/hrs/hrs-observing-times/hrs-observing-times.component";
import { HrsComponent } from "./proposal/instruments/hrs/hrs.component";
import { NirCalibrationComponent } from "./proposal/instruments/nir/nir-calibration/nir-calibration.component";
import { NirConfigurationComponent } from "./proposal/instruments/nir/nir-configuration/nir-configuration.component";
import { NirDitherStepsComponent } from "./proposal/instruments/nir/nir-dither-steps/nir-dither-steps.component";
import { NirGeneralInfoComponent } from "./proposal/instruments/nir/nir-general-info/nir-general-info.component";
import { NirComponent } from "./proposal/instruments/nir/nir.component";
import { ArcBibleComponent } from "./proposal/instruments/rss/arc-bible/arc-bible.component";
import { EtalonWavelengthsComponent } from "./proposal/instruments/rss/etalon-wavelengths/etalon-wavelengths.component";
import { FabryPerotComponent } from "./proposal/instruments/rss/fabry-perot/fabry-perot.component";
import { MosSlitMaskComponent } from "./proposal/instruments/rss/mos-slit-mask/mos-slit-mask.component";
import { PolarimetricImagingComponent } from "./proposal/instruments/rss/polarimetric-imaging/polarimetric-imaging.component";
import { PolarimetryComponent } from "./proposal/instruments/rss/polarimetry/polarimetry.component";
import { RssCalibrationComponent } from "./proposal/instruments/rss/rss-calibration/rss-calibration.component";
import { RssDetectorComponent } from "./proposal/instruments/rss/rss-detector/rss-detector.component";
import { RssGeneralInfoComponent } from "./proposal/instruments/rss/rss-general-info/rss-general-info.component";
import { RssSlitMaskComponent } from "./proposal/instruments/rss/rss-slit-mask/rss-slit-mask.component";
import { RssSpectroscopyComponent } from "./proposal/instruments/rss/rss-spectroscopy/rss-spectroscopy.component";
import { RssComponent } from "./proposal/instruments/rss/rss.component";
import { SalticamDetectorComponent } from "./proposal/instruments/salticam/salticam-detector-table/salticam-detector.component";
import { SalticamFiltersComponent } from "./proposal/instruments/salticam/salticam-filters/salticam-filters.component";
import { SalticamGeneralInfoComponent } from "./proposal/instruments/salticam/salticam-general-info/salticam-general-info.component";
import { SalticamObservationTimesComponent } from "./proposal/instruments/salticam/salticam-observation-times/salticam-observation-times.component";
import { SalticamComponent } from "./proposal/instruments/salticam/salticam.component";
import { InvestigatorsComponent } from "./proposal/investigators/investigators.component";
import { P1ConfigurationsComponent } from "./proposal/p1-details/p1-configurations/p1-configurations.component";
import { P1DetailsComponent } from "./proposal/p1-details/p1-details.component";
import { PhaseOneProposalDetailsTableComponent } from "./proposal/p1-details/phase-one-proposal-details/phase-one-proposal-details-table/phase-one-proposal-details-table.component";
import { PhaseOneProposalDetailsComponent } from "./proposal/p1-details/phase-one-proposal-details/phase-one-proposal-details.component";
import { PhaseOneTargetComponent } from "./proposal/p1-details/phase-one-target/phase-one-target.component";
import { StudentThesesComponent } from "./proposal/p1-details/students-theses/student-theses.component";
import { ProposalComponent } from "./proposal/proposal.component";
import { RequestedTimesComponent } from "./proposal/requested-time/requested-times.component";
import { TargetComponent } from "./proposal/target/target.component";
import { RegisterUserComponent } from "./register-user/register-user.component";
import { AuthGuardService } from "./service/auth-guard.service";
import { AuthenticationInterceptor } from "./service/authentication.interceptor.service";
import { AuthenticationService } from "./service/authentication.service";
import { BlockService } from "./service/block.service";
import { MosService } from "./service/mos.service";
import { ProposalService } from "./service/proposal.service";
import { RealAuthenticationService } from "./service/real/real-authentication.service";
import { RealBlockService } from "./service/real/real-block.service";
import { RealProposalService } from "./service/real/real-proposal.service";
import { ErrorIndicatorComponent } from "./shared/error-indicator/error-indicator.component";
import { LoadingIndicatorComponent } from "./shared/loading-indicator/loading-indicator.component";
import { LoadingSpinnerComponent } from "./shared/loading-spinner/loading-spinner.component";
import { PageMissingComponent } from "./shared/page-missing/page-missing.component";
import { SmallLoadingSpinnerComponent } from "./shared/small-loading-spinner/small-loading-spinner.component";
import { SortByDirective } from "./sort-by.directive";
import { SortDirective } from "./sort.directive";

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
    TimeAllocationsTableComponent,
    ChargedTimeComponent,
    ObservationCommentsComponent,
    RssSpectroscopyComponent,
    RssSlitMaskComponent,
    SalticamDetectorComponent,
    ArcBibleComponent,
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
    ForgotPasswordComponent,
    InlineLoginComponent,
    HomeUserComponent,
    HomeGuestComponent,
    NavigationBarComponent,
    ChangePasswordComponent,
    MosComponent,
    MosLegendComponent,
    MosBlocksTableComponent,
    MosMaskUpdateModalComponent,
    SortByArgsPipe,
    ObsoleteMasksComponent,
    PageMissingComponent,
    ManageUserProfileComponent,
    SmallLoadingSpinnerComponent,
    ProposalProgressComponent,
    RequestedObservingConditionsComponent,
    SubmittedTimeRequestsComponent,
    ProgressRequestFormComponent,
    NirComponent,
    NirGeneralInfoComponent,
    NirCalibrationComponent,
    NirConfigurationComponent,
    NirDitherStepsComponent,
    LoadingIndicatorComponent,
    ErrorIndicatorComponent,
    RegisterUserComponent,
    SortDirective,
    SortByDirective,
    P1DetailsComponent,
    PhaseOneTargetComponent,
    PhaseOneProposalDetailsComponent,
    ProposalSummaryComponent,
    ProposalDownloadComponent,
    ResponsibleAstronomerComponent,
    DetailsTableComponent,
    PhaseOneProposalDetailsTableComponent,
    RequestedTimesComponent,
    P1ConfigurationsComponent,
    StudentThesesComponent,
    EditProprietaryPeriodModalComponent,
    EditBlockStatusModalComponent,
    EditBlockVisitStatusModalComponent,
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
    CookieService,
    {
      provide: ErrorHandler,
      useValue: Sentry.createErrorHandler({ showDialog: true }),
    },
    { provide: Sentry.TraceService, deps: [Router] },
    {
      provide: APP_INITIALIZER,
      useFactory: () => () => {
        /* Do nothing */
      },
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
    MosService,
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
