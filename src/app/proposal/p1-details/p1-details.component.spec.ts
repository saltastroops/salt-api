import { ComponentFixture, TestBed } from '@angular/core/testing';

import { P1DetailsComponent } from './p1-details.component';

describe('PhaseOneComponent', () => {
  let component: P1DetailsComponent;
  let fixture: ComponentFixture<P1DetailsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ P1DetailsComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(P1DetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
