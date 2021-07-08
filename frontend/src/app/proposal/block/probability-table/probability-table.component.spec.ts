import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProbabilityTableComponent } from './probability-table.component';

describe('ProbabilityTableComponent', () => {
  let component: ProbabilityTableComponent;
  let fixture: ComponentFixture<ProbabilityTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProbabilityTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProbabilityTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
