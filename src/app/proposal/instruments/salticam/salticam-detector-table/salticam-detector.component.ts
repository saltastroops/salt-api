import { Component, OnInit, Input } from '@angular/core';
import { SalticamDetector } from '../../../../types/salticam';

@Component({
  selector: 'wm-salticam-detector',
  templateUrl: './salticam-detector.component.html',
  styleUrls: ['./salticam-detector.component.scss'],
})
export class SalticamDetectorComponent implements OnInit {
  @Input() detector!: SalticamDetector;
  constructor() {}

  ngOnInit(): void {}
}
