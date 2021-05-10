import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import {ProposalComponent} from "./proposal/proposal.component";
import {AppComponent} from "./app.component";
import {InvestigatorsComponent} from "./proposal/investigators/investigators.component";
import {HomeComponent} from "./home/home.component";

const routes: Routes = [
  {path: "", component: HomeComponent},
  {path: "hello", component: InvestigatorsComponent},
  {path: "proposal/:proposal-code", component: ProposalComponent}
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule]
})
export class AppRoutingModule { }
