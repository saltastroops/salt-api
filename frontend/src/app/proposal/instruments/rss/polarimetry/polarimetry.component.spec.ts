import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PolarimetryComponent } from './polarimetry.component';

describe('PolarimetryTableComponent', () => {
  let component: PolarimetryComponent;
  let fixture: ComponentFixture<PolarimetryComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PolarimetryComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PolarimetryComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
