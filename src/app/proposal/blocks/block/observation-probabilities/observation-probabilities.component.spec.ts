import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ObservationProbabilitiesComponent } from './observation-probabilities.component';

describe('ProbabilityTableComponent', () => {
  let component: ObservationProbabilitiesComponent;
  let fixture: ComponentFixture<ObservationProbabilitiesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ObservationProbabilitiesComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ObservationProbabilitiesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
