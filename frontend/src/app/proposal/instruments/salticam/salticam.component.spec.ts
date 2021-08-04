import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SalticamComponent } from './salticam.component';

describe('SalticamComponent', () => {
  let component: SalticamComponent;
  let fixture: ComponentFixture<SalticamComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SalticamComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SalticamComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
