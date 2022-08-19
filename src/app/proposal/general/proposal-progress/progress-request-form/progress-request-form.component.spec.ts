import { ComponentFixture, TestBed } from "@angular/core/testing";
import { ReactiveFormsModule } from "@angular/forms";

import { ProposalProgress } from "../../../../types/proposal";
import { ProgressRequestFormComponent } from "./progress-request-form.component";

describe("ProgressRequestFormComponent", () => {
  const progressReport: ProposalProgress = {
    requestedTime: null,
    semester: null,
    partnerRequestedPercentages: [
      {
        partnerCode: "2099-1-MLT-001",
        partnerName: "Partner",
        requestedPercentage: 10,
      },
    ],
    maximumSeeing: null,
    transparency: null,
    lastObservingConstraints: {
      seeing: 1,
      transparency: "Clear",
      description: "Description",
    },
    descriptionOfObservingConstraints: "Description",
    changeReason: null,
    summaryOfProposalStatus: null,
    strategyChanges: null,
    previousTimeRequests: [
      {
        semester: "2099-1",
        requestedTime: 30000,
        allocatedTime: 10000,
        observedTime: 3000,
      },
    ],
  };
  let component: ProgressRequestFormComponent;
  let fixture: ComponentFixture<ProgressRequestFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ReactiveFormsModule],
      declarations: [ProgressRequestFormComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProgressRequestFormComponent);
    component = fixture.componentInstance;
    component.progressReport = progressReport;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
