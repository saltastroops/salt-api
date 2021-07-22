import { ComponentFixture, TestBed } from '@angular/core/testing';

import { DetectorTableComponent } from './detector-table.component';

describe('DetectorTableComponent', () => {
  let component: DetectorTableComponent;
  let fixture: ComponentFixture<DetectorTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ DetectorTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(DetectorTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
