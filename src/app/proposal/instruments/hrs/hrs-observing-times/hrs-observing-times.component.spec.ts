import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrsObservingTimesComponent } from './hrs-observing-times.component';

describe('ObservingTimesTableComponent', () => {
  let component: HrsObservingTimesComponent;
  let fixture: ComponentFixture<HrsObservingTimesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrsObservingTimesComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HrsObservingTimesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
