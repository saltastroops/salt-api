import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RssDetectorTableComponent } from './rss-detector-table.component';

describe('DetectorTableComponent', () => {
  let component: RssDetectorTableComponent;
  let fixture: ComponentFixture<RssDetectorTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RssDetectorTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RssDetectorTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
