import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RssGeneralTableComponent } from './rss-general-table.component';

describe('RssGeneralTableComponent', () => {
  let component: RssGeneralTableComponent;
  let fixture: ComponentFixture<RssGeneralTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RssGeneralTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RssGeneralTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
