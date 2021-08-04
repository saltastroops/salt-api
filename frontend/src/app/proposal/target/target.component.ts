import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'wm-target',
  templateUrl: './target.component.html',
  styleUrls: ['./target.component.scss'],
})
export class TargetComponent implements OnInit {
  @Input() target: Target = {
    name: 'target name xxx',
    type: 'should be an enum',
    equinox: 2000,
    magnitude: '10-10',
    declination: '-20:12:12.1',
    rightAscension: '3:30:30.33',
  };
  constructor() {}

  ngOnInit(): void {}
}

interface Target {
  name: string;
  type: string; // TODO this should be an enum
  equinox: number;
  magnitude: string; // TODO need to verify
  declination: string;
  rightAscension: string;
}
