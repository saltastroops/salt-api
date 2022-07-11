import { ComponentFixture, TestBed } from "@angular/core/testing";

import { SubmittedTimeRequestsComponent } from "./submitted-time-requests.component";

describe("SubmittedTimeRequestsComponent", () => {
  let component: SubmittedTimeRequestsComponent;
  let fixture: ComponentFixture<SubmittedTimeRequestsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SubmittedTimeRequestsComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SubmittedTimeRequestsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
