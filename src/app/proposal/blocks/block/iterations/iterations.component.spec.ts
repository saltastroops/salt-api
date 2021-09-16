import { ComponentFixture, TestBed } from '@angular/core/testing';

import { IterationsComponent } from './iterations.component';

describe('IterationsComponent', () => {
  let component: IterationsComponent;
  let fixture: ComponentFixture<IterationsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [IterationsComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(IterationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
