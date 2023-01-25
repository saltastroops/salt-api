import { ComponentFixture, TestBed } from "@angular/core/testing";

import { PhaseOneProposalDetailsTableComponent } from "./phase-one-proposal-details-table.component";

describe("PhaseOneProposalDetailsTableComponent", () => {
  let component: PhaseOneProposalDetailsTableComponent;
  let fixture: ComponentFixture<PhaseOneProposalDetailsTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PhaseOneProposalDetailsTableComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PhaseOneProposalDetailsTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
