import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ObservationTimesComponent } from './observation-times.component';

describe('ObservatonTimesComponent', () => {
  let component: ObservationTimesComponent;
  let fixture: ComponentFixture<ObservationTimesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ObservationTimesComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ObservationTimesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
