import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PayloadConfigurationTableComponent } from './payload-configuration-table.component';

describe('PayloadConfigurationTableComponent', () => {
  let component: PayloadConfigurationTableComponent;
  let fixture: ComponentFixture<PayloadConfigurationTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PayloadConfigurationTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PayloadConfigurationTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
