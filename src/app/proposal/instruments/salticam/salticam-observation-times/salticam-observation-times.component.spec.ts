import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SalticamObservationTimesComponent } from './salticam-observation-times.component';

describe('ObservatonTimesComponent', () => {
  let component: SalticamObservationTimesComponent;
  let fixture: ComponentFixture<SalticamObservationTimesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SalticamObservationTimesComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SalticamObservationTimesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
