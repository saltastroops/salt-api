import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FiltersTableComponent } from './filters-table.component';

describe('FiltersTableComponent', () => {
  let component: FiltersTableComponent;
  let fixture: ComponentFixture<FiltersTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FiltersTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FiltersTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
