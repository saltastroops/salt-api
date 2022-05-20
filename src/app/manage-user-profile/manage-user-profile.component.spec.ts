import { ComponentFixture, TestBed } from "@angular/core/testing";

import { ManageUserProfileComponent } from "./manage-user-profile.component";

import { AuthenticationService } from "../service/authentication.service";
import { InstitutionService } from "../service/institution.service";
import { UserService } from "../service/user.service";
import {HttpClient, HttpHandler} from "@angular/common/http";
import {FormBuilder} from "@angular/forms";
import {of} from "rxjs";
import {User} from "../types/user";

describe("ManageUserProfileComponent", () => {
  const expectedUser: User = {
    id: 1,
    username: 'Jdoe',
    givenName: 'John',
    familyName: 'Doe',
    email: 'johndoe@exmaple.com',
    alternativeEmails: [],
    roles: [],
    affiliations: [
      {
        institutionId: 1,
        name: 'Institution A',
        partnerCode: 'RSA',
        department: ''
      }
    ]
  }
  let component: ManageUserProfileComponent;
  let fixture: ComponentFixture<ManageUserProfileComponent>;

  beforeEach(async () => {
    const getUserSpy = jasmine.createSpyObj('AuthenticationService', {
      'getUser': of(expectedUser)
    });

    await TestBed.configureTestingModule({
      declarations: [ManageUserProfileComponent],
      providers: [{ provide: AuthenticationService, useValue: getUserSpy }, InstitutionService, UserService, HttpClient, HttpHandler, FormBuilder]
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
