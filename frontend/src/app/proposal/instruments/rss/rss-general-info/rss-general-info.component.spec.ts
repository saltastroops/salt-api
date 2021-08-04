import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RssGeneralInfoComponent } from './rss-general-info.component';

describe('RssGeneralTableComponent', () => {
  let component: RssGeneralInfoComponent;
  let fixture: ComponentFixture<RssGeneralInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RssGeneralInfoComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RssGeneralInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
