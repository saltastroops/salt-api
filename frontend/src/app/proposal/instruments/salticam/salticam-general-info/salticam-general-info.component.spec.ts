import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SalticamGeneralInfoComponent } from './salticam-general-info.component';

describe('GeneralComponent', () => {
  let component: SalticamGeneralInfoComponent;
  let fixture: ComponentFixture<SalticamGeneralInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SalticamGeneralInfoComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SalticamGeneralInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
