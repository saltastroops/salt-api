import { ComponentFixture, TestBed } from "@angular/core/testing";

import { NirCalibrationComponent } from "./nir-calibration.component";

describe("NirCalibrationComponent", () => {
  let component: NirCalibrationComponent;
  let fixture: ComponentFixture<NirCalibrationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NirCalibrationComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NirCalibrationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
