import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HrsConfigurationTableComponent } from './hrs-configuration-table.component';

describe('ConfigurationTableComponent', () => {
  let component: HrsConfigurationTableComponent;
  let fixture: ComponentFixture<HrsConfigurationTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ HrsConfigurationTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HrsConfigurationTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
