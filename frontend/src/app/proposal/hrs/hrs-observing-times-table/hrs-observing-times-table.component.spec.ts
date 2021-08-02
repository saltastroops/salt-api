import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrsObservingTimesTableComponent } from './hrs-observing-times-table.component';

describe('ObservingTimesTableComponent', () => {
  let component: HrsObservingTimesTableComponent;
  let fixture: ComponentFixture<HrsObservingTimesTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HrsObservingTimesTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HrsObservingTimesTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
