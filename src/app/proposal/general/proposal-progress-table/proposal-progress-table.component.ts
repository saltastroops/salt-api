import { Component, Input } from '@angular/core';

@Component({
  selector: 'wm-proposal-progress-table',
  templateUrl: './proposal-progress-table.component.html',
  styleUrls: ['./proposal-progress-table.component.scss'],
})
export class ProposalProgressTableComponent {
  @Input() proposalProgress: string | null = null;
}
