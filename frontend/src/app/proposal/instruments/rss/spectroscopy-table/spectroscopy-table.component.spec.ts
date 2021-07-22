import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SpectroscopyTableComponent } from './spectroscopy-table.component';

describe('SpectroscopyTableComponent', () => {
  let component: SpectroscopyTableComponent;
  let fixture: ComponentFixture<SpectroscopyTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SpectroscopyTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SpectroscopyTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
