import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PriorityCommentComponent } from './priority-comment.component';

describe('BlockCommentComponent', () => {
  let component: PriorityCommentComponent;
  let fixture: ComponentFixture<PriorityCommentComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ PriorityCommentComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(PriorityCommentComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
