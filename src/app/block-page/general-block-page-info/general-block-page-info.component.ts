import { Component, Input, OnInit } from "@angular/core";
import { Proposal } from "../../types/proposal";

@Component({
  selector: 'wm-general-block-page-info',
  templateUrl: './general-block-page-info.component.html',
  styleUrls: ['./general-block-page-info.component.scss']
})
export class GeneralBlockPageInfoComponent implements OnInit {
  @Input() proposal!: Proposal;
  principalInvestigator = ""
  principalContact = ""
  liaisonSaltAstronomer = "None"

  ngOnInit(): void {
    this.proposal.investigators.forEach(i => {
      if(i.isPi){
        this.principalInvestigator = i.givenName + " " + i.familyName
      }
      if(i.isPc){
        this.principalContact = i.givenName + " " + i.familyName
      }
    })

    this.liaisonSaltAstronomer =
      this.proposal.generalInfo.liaisonSaltAstronomer
        ? this.proposal.generalInfo.liaisonSaltAstronomer.givenName
        + " "
        + this.proposal.generalInfo.liaisonSaltAstronomer?.familyName : "None"
  }
}
