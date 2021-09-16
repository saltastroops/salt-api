import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EtalonWavelengthsComponent } from './etalon-wavelengths.component';

describe('PolarimetryTableComponent', () => {
  let component: EtalonWavelengthsComponent;
  let fixture: ComponentFixture<EtalonWavelengthsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EtalonWavelengthsComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EtalonWavelengthsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
