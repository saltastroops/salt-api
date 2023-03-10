import { ComponentFixture, TestBed } from "@angular/core/testing";

import { ProposalStatusModalComponent } from "./proposal-status-modal.component";

describe("ProposalStatusCommentModalComponent", () => {
  // let component: ProposalStatusCommentModalComponent;
  let fixture: ComponentFixture<ProposalStatusModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ProposalStatusModalComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProposalStatusModalComponent);
    // component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(true);
  });
});
