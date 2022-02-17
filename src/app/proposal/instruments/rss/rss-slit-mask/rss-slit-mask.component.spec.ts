import { ComponentFixture, TestBed } from "@angular/core/testing";

import { RssSlitMaskComponent } from "./rss-slit-mask.component";

describe("SlitMaskComponent", () => {
  let component: RssSlitMaskComponent;
  let fixture: ComponentFixture<RssSlitMaskComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RssSlitMaskComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RssSlitMaskComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
