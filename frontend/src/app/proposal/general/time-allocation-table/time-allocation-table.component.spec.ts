import { ComponentFixture, TestBed } from '@angular/core/testing';

import { TimeAllocationTableComponent } from './time-allocation-table.component';

describe('AllocationTableComponent', () => {
  let component: TimeAllocationTableComponent;
  let fixture: ComponentFixture<TimeAllocationTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [TimeAllocationTableComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(TimeAllocationTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
