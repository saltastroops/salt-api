import {
  Component,
  Input,
  OnInit,
  Output,
  EventEmitter,
  OnDestroy,
} from '@angular/core';
import { Subject, Subscription } from 'rxjs';
import { debounceTime, distinctUntilChanged } from 'rxjs/operators';
import { BlockSummary } from '../../../../types/block';
import { byPropertiesOf } from '../../../../utils';

@Component({
  selector: 'wm-block-selection',
  templateUrl: './block-selection.component.html',
  styleUrls: ['./block-selection.component.scss'],
})
export class BlockSelectionComponent implements OnInit {
  @Input() blocks!: BlockSummary[];

  @Input() selectedBlock!: BlockSummary | null;

  @Output() selectEmitter = new EventEmitter<BlockSummary>();

  sortedBlocks: BlockSummary[] = [];

  constructor() {}

  ngOnInit(): void {
    this.sortedBlocks = this.blocks.sort(
      byPropertiesOf<BlockSummary>(['name'])
    );
  }

  get selectedIndex() {
    return this.selectedBlock
      ? this.sortedBlocks.indexOf(this.selectedBlock)
      : -1;
  }

  onSelect(event: Event) {
    const index = parseInt((event.target as HTMLSelectElement).value, 10);
    this.selectBlock(index);
  }

  selectBlock(index: number) {
    this.selectEmitter.emit(this.sortedBlocks[index]);
  }

  onInput(e: Event) {
    const selectedBlockName = (e.target as HTMLInputElement).value;
    const selectedIndex = this.sortedBlocks.findIndex(
      (block) => block.name === selectedBlockName
    );
    if (selectedIndex !== -1) {
      this.selectBlock(selectedIndex);
    }
  }
}
