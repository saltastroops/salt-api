import { Component, Input, OnInit } from '@angular/core';
import { Target } from '../../types/target';

@Component({
  selector: 'wm-target',
  templateUrl: './target.component.html',
  styleUrls: ['./target.component.scss'],
})
export class TargetComponent implements OnInit {
  @Input() target!: Target;

  constructor() {}

  ngOnInit(): void {}
}