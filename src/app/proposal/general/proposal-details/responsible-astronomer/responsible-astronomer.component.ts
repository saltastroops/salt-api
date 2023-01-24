import {Component, Input} from '@angular/core';
import {GeneralProposalInfo} from "../../../../types/proposal";

@Component({
  selector: 'wm-responsible-astronomer',
  templateUrl: './responsible-astronomer.component.html',
  styleUrls: ['./responsible-astronomer.component.scss']
})
export class ResponsibleAstronomerComponent {

  @Input() generalProposalInfo!: GeneralProposalInfo;


}
