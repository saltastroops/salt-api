import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TotalObservationTimeComponent } from './total-observation-time.component';

describe('TotalObsTimeComponent', () => {
  let component: TotalObservationTimeComponent;
  let fixture: ComponentFixture<TotalObservationTimeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ TotalObservationTimeComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TotalObservationTimeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
