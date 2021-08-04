import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ObservingConditionsComponent } from './observing-conditions.component';

describe('ObservingConditionsComponent', () => {
  let component: ObservingConditionsComponent;
  let fixture: ComponentFixture<ObservingConditionsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ObservingConditionsComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ObservingConditionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
