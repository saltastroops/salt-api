import { Component, EventEmitter, Input, Output } from "@angular/core";

@Component({
  selector: "wm-modal",
  templateUrl: "./modal.component.html",
  styleUrls: ["./modal.component.scss"],
})
export class ModalComponent {
  @Input() title!: string;
  @Input() isModalActive!: boolean;
  @Input() loading!: boolean;
  @Input() error!: string | undefined;
  @Input() warning!: string | undefined;
  @Output() submitContent = new EventEmitter<void>();
  @Output() closeModal = new EventEmitter<void>();

  submit(): void {
    this.submitContent.emit();
  }

  close(): void {
    this.closeModal.emit();
  }
}
