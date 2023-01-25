import { ComponentFixture, TestBed } from "@angular/core/testing";

import { PhaseOneRequestedTimeComponent } from "./phase-one-requested-time.component";

describe("PhaseOneRequestedTimeComponent", () => {
  let component: PhaseOneRequestedTimeComponent;
  let fixture: ComponentFixture<PhaseOneRequestedTimeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PhaseOneRequestedTimeComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PhaseOneRequestedTimeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
