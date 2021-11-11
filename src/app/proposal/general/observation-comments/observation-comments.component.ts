import { Component, Input, OnInit } from '@angular/core';
import { ObservationComment } from '../../../types/proposal';
import { parseISO } from 'date-fns';
import { ProposalService } from '../../../service/proposal.service';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';

@Component({
  selector: 'wm-observation-comments',
  templateUrl: './observation-comments.component.html',
  styleUrls: ['./observation-comments.component.scss'],
})
export class ObservationCommentsComponent implements OnInit {
  @Input() observationComments!: ObservationComment[];
  @Input() proposalCode!: string;
  parseDate = parseISO;
  commentForm!: FormGroup;
  submitted: boolean = false;
  isCommentInputOpen = false;
  loading = false;
  error: string | undefined = undefined;

  constructor(
    private formBuilder: FormBuilder,
    private proposalService: ProposalService
  ) {}

  ngOnInit(): void {
    this.commentForm = this.formBuilder.group({
      comment: ['', Validators.required],
    });
  }

  // convenience getter for easy access to form fields
  get f() {
    return this.commentForm.controls;
  }

  submitComment(): void {
    this.submitted = true;

    // stop here if form is invalid
    if (this.commentForm.invalid) {
      return;
    }

    this.error = undefined;
    this.loading = true;
    this.proposalService
      .submitObservationComment(this.proposalCode, this.f.comment.value)
      .subscribe(
        (data: ObservationComment[]) => {
          this.observationComments = data;
          this.loading = false;
          this.error = undefined;
          this.f.comment.reset('');
          this.closeCommentInput();
        },
        (error: string) => {
          this.error = error;
          this.loading = false;
        }
      );
  }

  openCommentInput(): void {
    this.isCommentInputOpen = true;
  }

  closeCommentInput(): void {
    this.isCommentInputOpen = false;
  }

  clearError(): void {
    this.error = undefined;
  }

  cancel(): void {
    this.f.comment.reset('');
    this.closeCommentInput();
    this.clearError();
  }
}
