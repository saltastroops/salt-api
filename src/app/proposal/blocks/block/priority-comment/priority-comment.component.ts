import { Component, Input, OnInit } from "@angular/core";

import { parseISO } from "date-fns";

import { Block } from "../../../../types/block";

@Component({
  selector: "wm-priority-comment",
  templateUrl: "./priority-comment.component.html",
  styleUrls: ["./priority-comment.component.scss"],
})
export class PriorityCommentComponent implements OnInit {
  @Input() block!: Block;
  latestSubmissionDate!: Date;

  ngOnInit(): void {
    this.latestSubmissionDate = parseISO(this.block.latestSubmissionDate);
  }
}
