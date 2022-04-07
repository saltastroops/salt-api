import { HttpClient } from "@angular/common/http";
import {
  HttpClientTestingModule,
  HttpTestingController,
} from "@angular/common/http/testing";
import { ComponentFixture, TestBed } from "@angular/core/testing";

import { ObsoleteMasksComponent } from "./obsolete-masks.component";

describe("ObsoleteMasksComponent", () => {
  let component: ObsoleteMasksComponent;
  let fixture: ComponentFixture<ObsoleteMasksComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ObsoleteMasksComponent],
      imports: [HttpClientTestingModule],
      providers: [HttpClient],
    }).compileComponents();
    TestBed.inject(HttpTestingController);
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ObsoleteMasksComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
