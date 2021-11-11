import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'wm-polarimetric-imaging',
  templateUrl: './polarimetric-imaging.component.html',
  styleUrls: ['./polarimetric-imaging.component.scss'],
})
export class PolarimetricImagingComponent {
  @Input() filter!: string;
  @Input() beamSplitterOrientation!: boolean;

  constructor() {}
}
