import { ComponentFixture, TestBed } from "@angular/core/testing";

import { HrsConfigRowComponent } from "./hrs-config-row.component";

describe("HrsConfigRowComponent", () => {
  let component: HrsConfigRowComponent;
  let fixture: ComponentFixture<HrsConfigRowComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [HrsConfigRowComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(HrsConfigRowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
