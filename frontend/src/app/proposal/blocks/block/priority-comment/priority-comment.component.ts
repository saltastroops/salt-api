import { Component, Input, OnInit } from '@angular/core';

@Component({
  selector: 'wm-priority-comment',
  templateUrl: './priority-comment.component.html',
  styleUrls: ['./priority-comment.component.scss'],
})
export class PriorityCommentComponent implements OnInit {
  @Input() comment: string = '';
  @Input() priority!: number;
  constructor() {}

  ngOnInit(): void {}
}