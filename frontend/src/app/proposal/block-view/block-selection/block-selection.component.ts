import { Component, Input, OnInit, Output, EventEmitter } from '@angular/core';
import { BlockIdentifier } from '../../../types';

@Component({
  selector: 'wm-block-selection',
  templateUrl: './block-selection.component.html',
  styleUrls: ['./block-selection.component.scss'],
})
export class BlockSelectionComponent implements OnInit {
  @Input() blocks!: Array<BlockIdentifier>;

  @Input() selectedBlock!: BlockIdentifier;

  @Output() select = new EventEmitter<BlockIdentifier>();

  constructor() {}

  get selectedIndex() {
    return this.blocks.indexOf(this.selectedBlock);
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
