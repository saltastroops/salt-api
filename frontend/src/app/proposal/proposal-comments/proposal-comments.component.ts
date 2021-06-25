import { Component, Input, OnInit } from '@angular/core';
import { ProposalComment } from '../../types';

@Component({
  selector: 'wm-proposal-comments',
  templateUrl: './proposal-comments.component.html',
  styleUrls: ['./proposal-comments.component.scss'],
})
export class ProposalCommentsComponent implements OnInit {
  @Input() proposalComments!: ProposalComment[];
  constructor() {}

  ngOnInit(): void {}
}
