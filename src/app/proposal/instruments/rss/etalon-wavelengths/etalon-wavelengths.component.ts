import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'wm-etalon-wvelengths',
  templateUrl: './etalon-wavelengths.component.html',
  styleUrls: ['./etalon-wavelengths.component.scss'],
})
export class EtalonWavelengthsComponent implements OnInit {
  @Input() etalonConfiguration!: number[];

  constructor() {}

  ngOnInit(): void {}
}
