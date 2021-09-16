import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrsConfigurationComponent } from './hrs-configuration.component';

describe('ConfigurationTableComponent', () => {
  let component: HrsConfigurationComponent;
  let fixture: ComponentFixture<HrsConfigurationComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrsConfigurationComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HrsConfigurationComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
