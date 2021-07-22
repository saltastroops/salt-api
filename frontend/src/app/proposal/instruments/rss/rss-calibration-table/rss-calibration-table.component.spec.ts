import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RssCalibrationTableComponent } from './rss-calibration-table.component';

describe('RssCalibrationTableComponent', () => {
  let component: RssCalibrationTableComponent;
  let fixture: ComponentFixture<RssCalibrationTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RssCalibrationTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RssCalibrationTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
