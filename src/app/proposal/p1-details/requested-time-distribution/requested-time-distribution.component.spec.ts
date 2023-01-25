import { ComponentFixture, TestBed } from "@angular/core/testing";

import { RequestedTimeDistributionComponent } from "./requested-time-distribution.component";

describe("RequestedTimeDistributionComponent", () => {
  let component: RequestedTimeDistributionComponent;
  let fixture: ComponentFixture<RequestedTimeDistributionComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RequestedTimeDistributionComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RequestedTimeDistributionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
