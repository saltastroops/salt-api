import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RssSpectroscopyComponent } from './rss-spectroscopy.component';

describe('SpectroscopyTableComponent', () => {
  let component: RssSpectroscopyComponent;
  let fixture: ComponentFixture<RssSpectroscopyComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RssSpectroscopyComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RssSpectroscopyComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
