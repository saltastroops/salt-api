import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { BlockSummary } from '../../../../types/block';

@Component({
  selector: 'wm-block-selection',
  templateUrl: './block-selection.component.html',
  styleUrls: ['./block-selection.component.scss'],
})
export class BlockSelectionComponent implements OnInit {
  @Input() blocks!: BlockSummary[];

  @Input() selectedBlock!: BlockSummary | null;

  @Output() select = new EventEmitter<BlockSummary>();

  constructor() {}

  get selectedIndex() {
    return this.selectedBlock ? this.blocks.indexOf(this.selectedBlock) : -1;
  }

  ngOnInit(): void {}

  onSelect(event: Event) {
    const index = parseInt((event.target as HTMLSelectElement).value, 10);
    this.selectBlock(index);
  }

  selectBlock(index: number) {
    this.select.emit(this.blocks[index]);
  }
}
