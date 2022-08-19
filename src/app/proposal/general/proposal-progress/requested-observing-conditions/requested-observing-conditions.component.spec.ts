import { ComponentFixture, TestBed } from "@angular/core/testing";

import { RequestedObservingConditionsComponent } from "./requested-observing-conditions.component";

describe("RequestedObservingConditionsComponent", () => {
  const lastObservingConstraints = {
    seeing: 1,
    transparency: "Clear",
    description: "Description",
  };
  let component: RequestedObservingConditionsComponent;
  let fixture: ComponentFixture<RequestedObservingConditionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RequestedObservingConditionsComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RequestedObservingConditionsComponent);
    component = fixture.componentInstance;
    component.lastObservingConstraints = lastObservingConstraints;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
