import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PhaseOneTargetComponent } from './phase-one-target.component';

describe('PhaseOneTargetComponent', () => {
  let component: PhaseOneTargetComponent;
  let fixture: ComponentFixture<PhaseOneTargetComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PhaseOneTargetComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PhaseOneTargetComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
