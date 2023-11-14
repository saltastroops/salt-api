import { ComponentFixture, TestBed } from "@angular/core/testing";

import { P1ProposalDetailsComponent } from "./p1-proposal-details.component";

describe("P1ProposalDetailsComponent", () => {
  let component: P1ProposalDetailsComponent;
  let fixture: ComponentFixture<P1ProposalDetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [P1ProposalDetailsComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(P1ProposalDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
