import { ComponentFixture, TestBed } from '@angular/core/testing';

import { EtalonConfigurationTableComponent } from './etalon-configuration-table.component';

describe('PolarimetryTableComponent', () => {
  let component: EtalonConfigurationTableComponent;
  let fixture: ComponentFixture<EtalonConfigurationTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ EtalonConfigurationTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EtalonConfigurationTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
