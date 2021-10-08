import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RssDetectorComponent } from './rss-detector.component';

describe('DetectorTableComponent', () => {
  let component: RssDetectorComponent;
  let fixture: ComponentFixture<RssDetectorComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RssDetectorComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RssDetectorComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
