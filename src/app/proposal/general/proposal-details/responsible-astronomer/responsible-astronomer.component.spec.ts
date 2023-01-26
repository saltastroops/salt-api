import { ComponentFixture, TestBed } from "@angular/core/testing";

import { ResponsibleAstronomerComponent } from "./responsible-astronomer.component";

describe("ResponsibleAstronomerComponent", () => {
  let component: ResponsibleAstronomerComponent;
  let fixture: ComponentFixture<ResponsibleAstronomerComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ResponsibleAstronomerComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ResponsibleAstronomerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
