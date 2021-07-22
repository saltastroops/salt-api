import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PolarimetryTableComponent } from './polarimetry-table.component';

describe('PolarimetryTableComponent', () => {
  let component: PolarimetryTableComponent;
  let fixture: ComponentFixture<PolarimetryTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PolarimetryTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PolarimetryTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
