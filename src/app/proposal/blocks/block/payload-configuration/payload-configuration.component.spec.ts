import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PayloadConfigurationComponent } from './payload-configuration.component';

describe('UseInTableComponent', () => {
  let component: PayloadConfigurationComponent;
  let fixture: ComponentFixture<PayloadConfigurationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [PayloadConfigurationComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PayloadConfigurationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
