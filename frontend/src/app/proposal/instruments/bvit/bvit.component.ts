import { Component, Input, OnInit } from '@angular/core';
import { Bvit } from '../../../types/bvit';

@Component({
  selector: 'wm-bvit',
  templateUrl: './bvit.component.html',
  styleUrls: ['./bvit.component.scss'],
})
export class BvitComponent implements OnInit {
  @Input() bvit!: Bvit;

  constructor() {}

  ngOnInit(): void {}
}
