import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrsGeneralInfoComponent } from './hrs-general-info.component';

describe('GeneralTableComponent', () => {
  let component: HrsGeneralInfoComponent;
  let fixture: ComponentFixture<HrsGeneralInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrsGeneralInfoComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HrsGeneralInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
