import {Component, Input} from '@angular/core';
import {RequestedTime} from "../../../types/proposal";

@Component({
  selector: 'wm-phase-one-requested-time',
  templateUrl: './phase-one-requested-time.component.html',
  styleUrls: ['./phase-one-requested-time.component.scss']
})
export class PhaseOneRequestedTimeComponent {

  @Input() requestedTime!: RequestedTime;

}
