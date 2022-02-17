import { ComponentFixture, TestBed } from "@angular/core/testing";

import { ProposalProgressTableComponent } from "./proposal-progress-table.component";

describe("ProposalProgressTableComponent", () => {
  let component: ProposalProgressTableComponent;
  let fixture: ComponentFixture<ProposalProgressTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ProposalProgressTableComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProposalProgressTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
