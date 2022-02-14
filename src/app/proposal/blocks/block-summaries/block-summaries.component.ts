import { Component, Input, OnInit } from '@angular/core';
import { BlockSummary } from '../../../types/block';
import { byPropertiesOf, sortArg } from '../../../utils';

@Component({
  selector: 'wm-block-summaries',
  templateUrl: './block-summaries.component.html',
  styleUrls: ['./block-summaries.component.scss'],
})
export class BlockSummariesComponent implements OnInit {
  @Input() blocks!: BlockSummary[];
  @Input() proposalCode!: string;
  isDesc = false;
  column = '';
  filteredByCompleted!: boolean;
  filteredByUnobservable!: boolean;
  filteredBlocks: BlockSummary[] = [];
  columnsSortDirections: { [columnName: string]: string | number | null } = {};

  ngOnInit(): void {
    this.filteredBlocks = this.blocks;
    this.filteredByCompleted =
      localStorage.getItem('filterByCompleted') == 'true';
    this.filteredByUnobservable =
      localStorage.getItem('filterByUnobservable') == 'true';

    (document.getElementById('filter-completed') as HTMLInputElement).checked =
      this.filteredByCompleted;
    (
      document.getElementById('filter-unobservable') as HTMLInputElement
    ).checked = this.filteredByUnobservable;

    this.filterBlocks();
    const sortableColumnElements =
      document.querySelectorAll('.sortable-column');
    sortableColumnElements.forEach((columnElement) => {
      const column = columnElement.getAttribute('data-testid');
      if (column) {
        this.columnsSortDirections[column] = '';
      }
    });
  }

  filterByCompleted(): void {
    this.filteredByCompleted = !this.filteredByCompleted;
    localStorage.setItem(
      'filterByCompleted',
      JSON.stringify(this.filteredByCompleted)
    );
    this.filterBlocks();
  }

  filterByUnobservable(): void {
    this.filteredByUnobservable = !this.filteredByUnobservable;
    localStorage.setItem(
      'filterByUnobservable',
      JSON.stringify(this.filteredByUnobservable)
    );
    this.filterBlocks();
  }

  filterBlocks(): void {
    let blocks = [...this.blocks];
    if (this.filteredByCompleted) {
      blocks = blocks.filter((block) => block.status.value !== 'Completed');
    }
    if (this.filteredByUnobservable) {
      blocks = blocks.filter(
        (block) =>
          block.acceptedObservations === block.requestedObservations ||
          block.remainingNights !== 0
      );
    }
    this.filteredBlocks = blocks;
  }

  isCompleted(block: BlockSummary): boolean {
    return (
      block.status.value === 'Completed' &&
      block.acceptedObservations === block.requestedObservations
    );
  }

  isUnobservable(block: BlockSummary): boolean {
    return (
      block.remainingNights === 0 &&
      block.acceptedObservations !== block.requestedObservations
    );
  }

  blockClass(block: BlockSummary): string {
    if (this.isCompleted(block)) {
      return 'completed-block';
    } else if (this.isUnobservable(block)) {
      return 'is-red-background';
    }
    return '';
  }

  blockDataTestAttribute(block: BlockSummary): string {
    if (this.isCompleted(block)) {
      return 'completed-block';
    } else if (this.isUnobservable(block)) {
      return 'unobservable-block';
    }
    return '';
  }

  onColumnClick(event: Event, columnName: sortArg<BlockSummary>): void {
    this.columnsSortDirections[columnName] =
      this.columnsSortDirections[columnName] === 'asc' ? 'desc' : 'asc';
    const direction = this.columnsSortDirections[columnName];

    this.isDesc = direction === 'desc';
    this.column = columnName;
    if (direction === 'asc') {
      this.filteredBlocks.sort(byPropertiesOf<BlockSummary>([columnName]));
    }
    if (direction === 'desc') {
      const column = <sortArg<BlockSummary>>('-' + columnName.toString());
      this.filteredBlocks.sort(byPropertiesOf<BlockSummary>([column]));
    }
  }

  sortableColumnClass(columnName: sortArg<BlockSummary>): {
    [key: string]: unknown;
  } {
    return {
      pointer: true,
      active: this.column == columnName,
      asc: !this.isDesc,
      desc: this.isDesc,
      sortable_column: true,
    };
  }
}
