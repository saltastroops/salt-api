import { ComponentFixture, TestBed } from "@angular/core/testing";

import { ManageUserProfileComponent } from "./manage-user-profile.component";

describe("EditContactInfoComponent", () => {
  let component: ManageUserProfileComponent;
  let fixture: ComponentFixture<ManageUserProfileComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ManageUserProfileComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ManageUserProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
