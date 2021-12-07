import { ComponentFixture, TestBed } from '@angular/core/testing';

import { HomeComponent } from './home.component';
import { AppComponent } from '../app.component';
import { FormBuilder } from '@angular/forms';
import { AuthenticationService } from '../service/authentication.service';
import { RealAuthenticationService } from '../service/real/real-authentication.service';
import { HttpClient, HttpHandler } from '@angular/common/http';

describe('HomeComponent', () => {
  let component: HomeComponent;
  let fixture: ComponentFixture<HomeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HomeComponent],
      providers: [
        FormBuilder,
        HttpClient,
        HttpHandler,
        { provide: AuthenticationService, useClass: RealAuthenticationService },
      ],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HomeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
