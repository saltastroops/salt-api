import { ComponentFixture, TestBed } from "@angular/core/testing";

import { NirGeneralInfoComponent } from "./nir-general-info.component";

describe("NirGeneralInfoComponent", () => {
  let component: NirGeneralInfoComponent;
  let fixture: ComponentFixture<NirGeneralInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NirGeneralInfoComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(NirGeneralInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
