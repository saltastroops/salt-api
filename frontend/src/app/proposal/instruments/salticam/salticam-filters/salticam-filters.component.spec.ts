import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SalticamFiltersComponent } from './salticam-filters.component';

describe('FiltersTableComponent', () => {
  let component: SalticamFiltersComponent;
  let fixture: ComponentFixture<SalticamFiltersComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SalticamFiltersComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SalticamFiltersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
