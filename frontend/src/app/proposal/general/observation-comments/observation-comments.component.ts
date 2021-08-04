import { Component, Input, OnInit } from '@angular/core';
import { ObservationComment } from '../../../types/proposal';
import { parseISO } from 'date-fns';

@Component({
  selector: 'wm-proposal-comments',
  templateUrl: './observation-comments.component.html',
  styleUrls: ['./observation-comments.component.scss'],
})
export class ObservationCommentsComponent implements OnInit {
  @Input() observationComments!: ObservationComment[];
  parseDate = parseISO;

  constructor() {}

  ngOnInit(): void {}
}
