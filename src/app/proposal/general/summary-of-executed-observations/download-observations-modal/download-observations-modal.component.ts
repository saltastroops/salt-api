import { Component, EventEmitter, Output } from "@angular/core";

import { Observation } from "../summary-of-executed-observations.component";

@Component({
  selector: "wm-download-observations-modal",
  templateUrl: "./download-observations-modal.component.html",
  styleUrls: ["./download-observations-modal.component.scss"],
})
export class DownloadObservationsModalComponent {
  @Output() closeModal = new EventEmitter<void>();
  observations!: Observation[];
  includeCalibrations!: boolean;
  isModalActive = false;

  openModal(observations: Observation[], includeCalibrations: boolean): void {
    this.isModalActive = true;
    this.observations = observations;
    this.includeCalibrations = includeCalibrations;
  }

  _closeModal(): void {
    this.isModalActive = false;
    this.closeModal.emit();
  }
}
