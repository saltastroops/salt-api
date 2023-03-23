import { Component, Input, OnInit } from "@angular/core";
import { AbstractControl, FormBuilder } from "@angular/forms";

import { ProposalService } from "../../../../../service/proposal.service";
import { SaltAstronomersService } from "../../../../../service/salt-astronomers.service";
import { Proposal } from "../../../../../types/proposal";
import { UserListItem } from "../../../../../types/user";
import { AutoUnsubscribe } from "../../../../../utils";

@Component({
  selector: "wm-liaison-astronomer-modal",
  templateUrl: "./liaison-astronomer-modal.component.html",
  styleUrls: ["./liaison-astronomer-modal.component.scss"],
})
@AutoUnsubscribe()
export class LiaisonAstronomerModalComponent implements OnInit {
  @Input() proposal!: Proposal;
  loadingAstronomers = false;
  submitting = false;
  astronomersError: string | null = null;
  updateError: string | null = null;
  saltAstronomers!: UserListItem[] | null;
  initialSaltAstronomerId: string | null = null;
  isUpdated = false;
  isModalActive = false;
  saltAstronomerForm = this.fb.group({
    selectedSaltAstronomer: [{ value: "", disabled: false }],
  });

  constructor(
    private saltAstronomersService: SaltAstronomersService,
    private proposalService: ProposalService,
    private fb: FormBuilder,
  ) {}

  ngOnInit(): void {
    this.loadingAstronomers = true;
    this.saltAstronomersService.getSaltAstronomers().subscribe(
      (saltAstronomers) => {
        this.saltAstronomers = saltAstronomers;

        this.initialSaltAstronomerId = this.proposal.generalInfo
          .liaisonSaltAstronomer
          ? `${this.proposal.generalInfo.liaisonSaltAstronomer.id}`
          : "";
        this.selectedSaltAstronomer.setValue(this.initialSaltAstronomerId, {
          onlySelf: true,
        });
        this.loadingAstronomers = false;
      },
      () => {
        this.loadingAstronomers = false;
        this.astronomersError = "Failed to fetch SALT Astronomers.";
      },
    );
  }

  openModal(): void {
    this.isModalActive = true;
  }

  changeSaltAstronomer(saltAstronomerId: string): void {
    this.selectedSaltAstronomer.setValue(`${saltAstronomerId}`, {
      onlySelf: true,
    });
  }

  get selectedSaltAstronomer(): AbstractControl {
    return this.saltAstronomerForm.controls.selectedSaltAstronomer;
  }

  closeModal(): void {
    if (!this.submitting) {
      this.isModalActive = false;
      this.astronomersError = null;
      this.updateError = null;
    }
  }

  submit(): void {
    this.submitting = true;
    const saltAstronomerId =
      this.selectedSaltAstronomer.value == ""
        ? null
        : this.selectedSaltAstronomer.value;

    this.proposalService
      .updateLiaisonAstronomer(this.proposal.proposalCode, saltAstronomerId)
      .subscribe(
        (liaisonAstronomer) => {
          this.isUpdated = true;
          this.initialSaltAstronomerId = saltAstronomerId;
          this.submitting = false;
          this.proposal.generalInfo.liaisonSaltAstronomer = liaisonAstronomer;
          this.closeModal();
        },
        () => {
          this.isUpdated = false;
          this.updateError = "Failed to update the liaison SALT astronomer!";
          this.submitting = false;
        },
      );
  }
}
