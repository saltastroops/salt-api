import { Component, Input } from '@angular/core';
import { SalticamDetector } from '../../../../types/salticam';

@Component({
  selector: 'wm-salticam-detector',
  templateUrl: './salticam-detector.component.html',
  styleUrls: ['./salticam-detector.component.scss'],
})
export class SalticamDetectorComponent {
  @Input() detector!: SalticamDetector;
}
