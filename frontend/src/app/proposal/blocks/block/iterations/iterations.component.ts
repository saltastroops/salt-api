import { Component, Input, OnInit } from '@angular/core';
import { Block } from '../../../../types/block';

@Component({
  selector: 'wm-iterations',
  templateUrl: './iterations.component.html',
  styleUrls: ['./iterations.component.scss'],
})
export class IterationsComponent implements OnInit {
  @Input() block!: Block;

  acceptedObservations!: number;

  rejectedObservations!: number;

  constructor() {}

  ngOnInit(): void {
    this.acceptedObservations = this.block.executedObservations.filter(
      (o) => o.accepted
    ).length;
    this.rejectedObservations =
      this.block.executedObservations.length - this.acceptedObservations;
  }
}
