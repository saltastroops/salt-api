import { Component, Input, OnInit } from '@angular/core';
import { RssPolarimetryPattern } from '../../../../types/rss';

@Component({
  selector: 'wm-polarimetry',
  templateUrl: './polarimetry.component.html',
  styleUrls: ['./polarimetry.component.scss'],
})
export class PolarimetryComponent implements OnInit {
  @Input() pattern!: RssPolarimetryPattern;

  constructor() {}

  ngOnInit(): void {}
}