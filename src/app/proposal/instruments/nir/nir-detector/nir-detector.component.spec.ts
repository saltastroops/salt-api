import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NirDetectorComponent } from './nir-detector.component';

describe('NirDetectorComponent', () => {
  let component: NirDetectorComponent;
  let fixture: ComponentFixture<NirDetectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NirDetectorComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NirDetectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
