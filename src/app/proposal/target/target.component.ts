import { Component, Input, OnInit } from '@angular/core';
import { Target } from '../../types/target';
import { degreesToDms, degreesToHms } from '../../utils';

@Component({
  selector: 'wm-target',
  templateUrl: './target.component.html',
  styleUrls: ['./target.component.scss'],
})
export class TargetComponent implements OnInit {
  @Input() target!: Target;

  rightAscension!: string;
  declination!: string;

  constructor() {}

  ngOnInit(): void {
    if (!this.target.nonSidereal) {
      this.rightAscension = degreesToHms(
        this.target.coordinates!.rightAscension,
        2
      );
      this.declination = degreesToDms(this.target.coordinates!.declination, 2);
    } else if (this.target.horizonsIdentifier) {
      this.rightAscension = 'N/A';
      this.declination = 'N/A (' + this.target.horizonsIdentifier + ')';
    } else {
      this.rightAscension = 'N/A';
      this.declination = 'N/A (Non-sidereal)';
    }
  }
}
