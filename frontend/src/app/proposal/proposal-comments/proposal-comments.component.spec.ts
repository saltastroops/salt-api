import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProposalCommentsComponent } from './proposal-comments.component';

describe('ProposalCommentComponent', () => {
  let component: ProposalCommentsComponent;
  let fixture: ComponentFixture<ProposalCommentsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ProposalCommentsComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProposalCommentsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
