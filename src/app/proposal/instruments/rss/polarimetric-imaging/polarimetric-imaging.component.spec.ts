import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PolarimetricImagingComponent } from './polarimetric-imaging.component';

describe('PolarimetryImagingTableComponent', () => {
  let component: PolarimetricImagingComponent;
  let fixture: ComponentFixture<PolarimetricImagingComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PolarimetricImagingComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PolarimetricImagingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
