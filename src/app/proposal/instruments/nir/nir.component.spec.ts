import { ComponentFixture, TestBed } from '@angular/core/testing';

import { NirComponent } from './nir.component';

describe('NirComponent', () => {
  let component: NirComponent;
  let fixture: ComponentFixture<NirComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ NirComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NirComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
