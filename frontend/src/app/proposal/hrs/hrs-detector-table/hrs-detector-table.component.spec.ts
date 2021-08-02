import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrsDetectorTableComponent } from './hrs-detector-table.component';

describe('BlueDetectorTableComponent', () => {
  let component: HrsDetectorTableComponent;
  let fixture: ComponentFixture<HrsDetectorTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HrsDetectorTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HrsDetectorTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
