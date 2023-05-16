import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";

import { HomeComponent } from "./home/home.component";
import { ChangePasswordComponent } from "./login/change-password/change-password.component";
import { ForgotPasswordComponent } from "./login/forgot-password/forgot-password.component";
import { LoginComponent } from "./login/login.component";
import { SwitchUserComponent } from "./login/switch-user/switch-user.component";
import { ManageUserProfileComponent } from "./manage-user-profile/manage-user-profile.component";
import { MosComponent } from "./mos/mos.component";
import { ProposalComponent } from "./proposal/proposal.component";
import { RegisterUserComponent } from "./register-user/register-user.component";
import { AuthGuardService } from "./service/auth-guard.service";
import { PageMissingComponent } from "./shared/page-missing/page-missing.component";
import { SoPageComponent } from "./so-page/so-page.component";

const routes: Routes = [
  { path: "", component: HomeComponent },
  { path: "login", component: LoginComponent },
  { path: "register", component: RegisterUserComponent },
  {
    path: "proposal/:proposal-code",
    component: ProposalComponent,
    canActivate: [AuthGuardService],
  },
  { path: "forgot-password", component: ForgotPasswordComponent },
  { path: "change-password/:token", component: ChangePasswordComponent },
  { path: "mos", component: MosComponent, canActivate: [AuthGuardService] },
  { path: "so-pages", component: SoPageComponent },
  {
    path: "manage-user-profile",
    component: ManageUserProfileComponent,
    canActivate: [AuthGuardService],
  },

  { path: "so-pages", component: PageMissingComponent },
  { path: "investigators", component: PageMissingComponent },
  {
    path: "switch-user",
    component: SwitchUserComponent,
    canActivate: [AuthGuardService],
  },
  { path: "page-missing", component: PageMissingComponent },
  { path: "**", redirectTo: "/page-missing", pathMatch: "full" },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
