import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RssCalibrationComponent } from './rss-calibration.component';

describe('RssCalibrationTableComponent', () => {
  let component: RssCalibrationComponent;
  let fixture: ComponentFixture<RssCalibrationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RssCalibrationComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RssCalibrationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
