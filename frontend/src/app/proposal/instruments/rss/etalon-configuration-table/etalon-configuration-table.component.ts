import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'wm-polarimetry-table',
  templateUrl: './etalon-configuration-table.component.html',
  styleUrls: ['./etalon-configuration-table.component.scss']
})
export class EtalonConfigurationTableComponent implements OnInit {
  @Input() etalonConfiguration: { wavelength: number }[] = [
    {wavelength: 48000},
    {wavelength: 48000},
    {wavelength: 48000},
    {wavelength: 48000},
    {wavelength: 48000},
    {wavelength: 48000},
    {wavelength: 48000},
  ];

  constructor() {
  }

  ngOnInit(): void {
  }

}
