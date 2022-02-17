import { ComponentFixture, TestBed } from "@angular/core/testing";

import { ArcBibleComponent } from "./arc-bible.component";

describe("ArcBibleTableComponent", () => {
  let component: ArcBibleComponent;
  let fixture: ComponentFixture<ArcBibleComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ArcBibleComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ArcBibleComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
