import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PolarimetricImagingTableComponent } from './polarimetric-imaging-table.component';

describe('PolarimetryImagingTableComponent', () => {
  let component: PolarimetricImagingTableComponent;
  let fixture: ComponentFixture<PolarimetricImagingTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PolarimetricImagingTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PolarimetricImagingTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
