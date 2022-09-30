import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NirSpectroscopyComponent } from './nir-spectroscopy.component';

describe('NirSpectroscopyComponent', () => {
  let component: NirSpectroscopyComponent;
  let fixture: ComponentFixture<NirSpectroscopyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NirSpectroscopyComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NirSpectroscopyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
