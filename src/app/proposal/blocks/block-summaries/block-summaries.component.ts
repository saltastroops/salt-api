import { Component, Input, OnInit } from '@angular/core';
import { BlockSummary } from '../../../types/block';

@Component({
  selector: 'wm-block-summaries',
  templateUrl: './block-summaries.component.html',
  styleUrls: ['./block-summaries.component.scss'],
})
export class BlockSummariesComponent {
  @Input() blocks!: BlockSummary[];
  @Input() proposalCode!: string;
  constructor() {}
}
