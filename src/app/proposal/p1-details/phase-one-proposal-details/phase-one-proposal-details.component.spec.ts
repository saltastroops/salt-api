import { ComponentFixture, TestBed } from "@angular/core/testing";

import { PhaseOneProposalDetailsComponent } from "./phase-one-proposal-details.component";

describe("PhaseOneProposalDetailsComponent", () => {
  let component: PhaseOneProposalDetailsComponent;
  let fixture: ComponentFixture<PhaseOneProposalDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PhaseOneProposalDetailsComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PhaseOneProposalDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
