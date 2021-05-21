import { ComponentFixture, TestBed } from '@angular/core/testing';

import { BlockSummariesComponent } from './block-summaries.component';

describe('BlockSummaryComponent', () => {
  let component: BlockSummariesComponent;
  let fixture: ComponentFixture<BlockSummariesComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [BlockSummariesComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(BlockSummariesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
