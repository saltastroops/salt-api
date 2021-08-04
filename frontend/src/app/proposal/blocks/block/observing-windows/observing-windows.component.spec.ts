import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ObservingWindowsComponent } from './observing-windows.component';

describe('ObservingWindowComponent', () => {
  let component: ObservingWindowsComponent;
  let fixture: ComponentFixture<ObservingWindowsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ObservingWindowsComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ObservingWindowsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
