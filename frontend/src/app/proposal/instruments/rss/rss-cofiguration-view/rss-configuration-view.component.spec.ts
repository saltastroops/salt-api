import { ComponentFixture, TestBed } from '@angular/core/testing';

import { RssConfigurationViewComponent } from './rss-configuration-view.component';

describe('InstrumentCofigurationComponent', () => {
  let component: RssConfigurationViewComponent;
  let fixture: ComponentFixture<RssConfigurationViewComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ RssConfigurationViewComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RssConfigurationViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
