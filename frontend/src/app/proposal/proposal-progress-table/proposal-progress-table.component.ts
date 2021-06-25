import {Component, Input, OnInit} from '@angular/core';

@Component({
  selector: 'wm-proposal-progress-table',
  templateUrl: './proposal-progress-table.component.html',
  styleUrls: ['./proposal-progress-table.component.scss']
})
export class ProposalProgressTableComponent implements OnInit {
  @Input() proposalProgress: string | null = null;
  constructor() { }

  ngOnInit(): void {
  }

}
