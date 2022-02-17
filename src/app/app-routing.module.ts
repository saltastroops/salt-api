import { NgModule } from "@angular/core";
import { RouterModule, Routes } from "@angular/router";

import { HomeComponent } from "./home/home.component";
import { ChangePasswordComponent } from "./login/change-password/change-password.component";
import { ForgotPasswordComponent } from "./login/forgot-password/forgot-password.component";
import { LoginComponent } from "./login/login.component";
import { ProposalComponent } from "./proposal/proposal.component";
import { AuthGuardService } from "./service/auth-guard.service";

const routes: Routes = [
  { path: "", component: HomeComponent },
  { path: "login", component: LoginComponent },
  {
    path: "proposal/:proposal-code",
    component: ProposalComponent,
    canActivate: [AuthGuardService],
  },
  { path: "forgot-password", component: ForgotPasswordComponent },
  { path: "change-password/:token", component: ChangePasswordComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
