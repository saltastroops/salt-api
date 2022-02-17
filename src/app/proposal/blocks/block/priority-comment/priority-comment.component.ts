import { Component, Input } from "@angular/core";

@Component({
  selector: "wm-priority-comment",
  templateUrl: "./priority-comment.component.html",
  styleUrls: ["./priority-comment.component.scss"],
})
export class PriorityCommentComponent {
  @Input() comment = "";
  @Input() priority!: number;
}
