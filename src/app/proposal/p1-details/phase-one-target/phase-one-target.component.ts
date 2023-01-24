import {Component, Input} from '@angular/core';
import {Phase1Target} from "../../../types/target";
import {degreesToDms, degreesToHms} from "../../../utils";

@Component({
  selector: 'wm-phase-one-target',
  templateUrl: './phase-one-target.component.html',
  styleUrls: ['./phase-one-target.component.scss']
})
export class PhaseOneTargetComponent {
  @Input() phase1Targets!: Phase1Target[] | null;
  degreeToHMS = degreesToHms
  degreesToDms = degreesToDms
}
