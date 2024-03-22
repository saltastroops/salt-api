import { ComponentFixture, TestBed } from "@angular/core/testing";

import { RequestVerificationLinkComponent } from "./request-verification-link.component";

describe("RequestActivationLinkComponent", () => {
  let component: RequestVerificationLinkComponent;
  let fixture: ComponentFixture<RequestVerificationLinkComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [RequestVerificationLinkComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(RequestVerificationLinkComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
