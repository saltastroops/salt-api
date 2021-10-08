import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrsDetectorComponent } from './hrs-detector.component';

describe('BlueDetectorTableComponent', () => {
  let component: HrsDetectorComponent;
  let fixture: ComponentFixture<HrsDetectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrsDetectorComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HrsDetectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
