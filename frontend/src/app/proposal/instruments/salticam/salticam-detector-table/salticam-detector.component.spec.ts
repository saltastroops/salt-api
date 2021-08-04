import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SalticamDetectorComponent } from './salticam-detector.component';

describe('DetectorTableComponent', () => {
  let component: SalticamDetectorComponent;
  let fixture: ComponentFixture<SalticamDetectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SalticamDetectorComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SalticamDetectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
