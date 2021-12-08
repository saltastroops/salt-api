import { Component, Input } from '@angular/core';
import { Salticam } from '../../../types/salticam';
import { PayloadConfiguration } from '../../../types/observation';

@Component({
  selector: 'wm-salticam',
  templateUrl: './salticam.component.html',
  styleUrls: ['./salticam.component.scss'],
})
export class SalticamComponent {
  @Input() salticam!: Salticam;
  @Input() payloadConfiguration!: PayloadConfiguration;
}
