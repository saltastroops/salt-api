import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrsGeneralTableComponent } from './hrs-general-table.component';

describe('GeneralTableComponent', () => {
  let component: HrsGeneralTableComponent;
  let fixture: ComponentFixture<HrsGeneralTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HrsGeneralTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HrsGeneralTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
