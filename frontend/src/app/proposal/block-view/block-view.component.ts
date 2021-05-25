import { Component, Input, OnInit } from '@angular/core';
import { BlockIdentifier } from '../../types';

@Component({
  selector: 'wm-block-view',
  templateUrl: './block-view.component.html',
  styleUrls: ['./block-view.component.scss'],
})
export class BlockViewComponent implements OnInit {
  @Input() blocks: Array<BlockIdentifier> = [
    { id: 45, name: 'A' },
    { id: 56, name: 'B' },
    { id: 78, name: 'C' },
  ];

  selectedBlock!: BlockIdentifier;

  constructor() {}

  ngOnInit(): void {
    this.selectedBlock = this.blocks[0];
  }

  showBlock(block: { id: number; name: string }) {
    this.selectedBlock = block;
  }
}
