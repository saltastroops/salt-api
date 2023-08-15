import { ComponentFixture, TestBed } from "@angular/core/testing";

import { FinderChartViewComponent } from "./finder-chart-view.component";

describe("FinderChatViewComponent", () => {
  let component: FinderChartViewComponent;
  let fixture: ComponentFixture<FinderChartViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FinderChartViewComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FinderChartViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
