import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ObservationCommentsComponent } from './observation-comments.component';

describe('ProposalCommentComponent', () => {
  let component: ObservationCommentsComponent;
  let fixture: ComponentFixture<ObservationCommentsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ObservationCommentsComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ObservationCommentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
