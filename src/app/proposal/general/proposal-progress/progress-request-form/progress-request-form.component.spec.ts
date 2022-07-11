import { ComponentFixture, TestBed } from "@angular/core/testing";

import { ProgressRequestFormComponent } from "./progress-request-form.component";

describe("ProgressRequestFormComponent", () => {
  let component: ProgressRequestFormComponent;
  let fixture: ComponentFixture<ProgressRequestFormComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ProgressRequestFormComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProgressRequestFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
