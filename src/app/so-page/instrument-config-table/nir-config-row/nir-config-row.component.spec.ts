import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NirConfigRowComponent } from './nir-config-row.component';

describe('NirConfigRowComponent', () => {
  let component: NirConfigRowComponent;
  let fixture: ComponentFixture<NirConfigRowComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NirConfigRowComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NirConfigRowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
