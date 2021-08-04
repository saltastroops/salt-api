import { Component, Input, OnInit } from '@angular/core';
import { Hrs } from '../../../types/hrs';

@Component({
  selector: 'wm-hrs',
  templateUrl: './hrs.component.html',
  styleUrls: ['./hrs.component.scss'],
})
export class HrsComponent implements OnInit {
  @Input() hrs!: Hrs;

  constructor() {}

  ngOnInit(): void {}
}
