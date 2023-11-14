import { ComponentFixture, TestBed } from "@angular/core/testing";

import { P1ProposalStatusModalComponent } from "./p1-proposal-status-modal.component";

describe("P1ProposalStatusModalComponent", () => {
  let component: P1ProposalStatusModalComponent;
  let fixture: ComponentFixture<P1ProposalStatusModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [P1ProposalStatusModalComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(P1ProposalStatusModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
