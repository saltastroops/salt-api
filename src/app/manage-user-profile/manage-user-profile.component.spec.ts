import { HttpClient, HttpHandler } from "@angular/common/http";
import { ComponentFixture, TestBed } from "@angular/core/testing";
import { UntypedFormBuilder } from "@angular/forms";

import { of } from "rxjs";

import { AuthenticationService } from "../service/authentication.service";
import { InstitutionService } from "../service/institution.service";
import { UserService } from "../service/user.service";
import { User } from "../types/user";
import { ManageUserProfileComponent } from "./manage-user-profile.component";

describe("ManageUserProfileComponent", () => {
  const expectedUser: User = {
    id: 1,
    username: "Jdoe",
    givenName: "John",
    familyName: "Doe",
    email: "johndoe@exmaple.com",
    alternativeEmails: [],
    roles: [],
    affiliations: [
      {
        institutionId: 1,
        name: "Institution A",
        partnerCode: "RSA",
        partnerName: "Partner A",
        department: "",
      },
    ],
  };
  let component: ManageUserProfileComponent;
  let fixture: ComponentFixture<ManageUserProfileComponent>;

  beforeEach(async () => {
    const getUserSpy = jasmine.createSpyObj("AuthenticationService", {
      getUser: of(expectedUser),
    });

    await TestBed.configureTestingModule({
      declarations: [ManageUserProfileComponent],
      providers: [
        { provide: AuthenticationService, useValue: getUserSpy },
        InstitutionService,
        UserService,
        HttpClient,
        HttpHandler,
        UntypedFormBuilder,
      ],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ManageUserProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    component.user$.subscribe((user) => {
      expect(user).toEqual(expectedUser);
    });
    // authServiceSpy.getUser.and.returnValue(of(expectedUser))
    expect(component).toBeTruthy();
  });
});
