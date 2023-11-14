import { ComponentFixture, TestBed } from "@angular/core/testing";

import { P1DetailsTableComponent } from "./p1-details-table.component";

describe("P1DetailsTableComponent", () => {
  let component: P1DetailsTableComponent;
  let fixture: ComponentFixture<P1DetailsTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [P1DetailsTableComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(P1DetailsTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
