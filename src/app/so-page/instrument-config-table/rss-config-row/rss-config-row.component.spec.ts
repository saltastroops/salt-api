import { ComponentFixture, TestBed } from "@angular/core/testing";

import { RssConfigRowComponent } from "./rss-config-row.component";

describe("RssConfigRowComponent", () => {
  let component: RssConfigRowComponent;
  let fixture: ComponentFixture<RssConfigRowComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RssConfigRowComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RssConfigRowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
