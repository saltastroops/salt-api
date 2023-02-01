import { ComponentFixture, TestBed } from "@angular/core/testing";

import { TimeAllocationsTableComponent } from "./time-allocations-table.component";

describe("AllocationsTableComponent", () => {
  let component: TimeAllocationsTableComponent;
  let fixture: ComponentFixture<TimeAllocationsTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TimeAllocationsTableComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TimeAllocationsTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
