import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'wm-polarimetry-table',
  templateUrl: './polarimetry-table.component.html',
  styleUrls: ['./polarimetry-table.component.scss']
})
export class PolarimetryTableComponent implements OnInit {
  @Input() polarimetry: PolarimetryPattern = {
    pattern: 'Linear',
    wavePlateAngles: [
      {halfWavePattern: 0, quarterWavePattern: null},
      {halfWavePattern: 45, quarterWavePattern: null},
      {halfWavePattern: 22, quarterWavePattern: null},
      {halfWavePattern: 75, quarterWavePattern: null},
    ]
  };

  constructor() { }

  ngOnInit(): void {
  }

}

// TODO this should go to the RSS Types
export interface PolarimetryPattern {
  pattern: string;  // TODO this should be an enum
  wavePlateAngles: {
    halfWavePattern: number | null;
    quarterWavePattern: number | null;
  }[];
}
