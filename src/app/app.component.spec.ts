import { HttpClient, HttpHandler } from "@angular/common/http";
import { TestBed } from "@angular/core/testing";
import { FormBuilder } from "@angular/forms";
import { RouterTestingModule } from "@angular/router/testing";

import { AppComponent } from "./app.component";
import { AuthenticationService } from "./service/authentication.service";
import { RealAuthenticationService } from "./service/real/real-authentication.service";

describe("AppComponent", () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [RouterTestingModule],
      providers: [
        FormBuilder,
        HttpClient,
        HttpHandler,
        { provide: AuthenticationService, useClass: RealAuthenticationService },
      ],
      declarations: [AppComponent],
    }).compileComponents();
  });

  it("should create the app", () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app).toBeTruthy();
  });

  it(`should have as title 'Web Manager'`, () => {
    const fixture = TestBed.createComponent(AppComponent);
    const app = fixture.componentInstance;
    expect(app.title).toEqual("Web Manager");
  });
});