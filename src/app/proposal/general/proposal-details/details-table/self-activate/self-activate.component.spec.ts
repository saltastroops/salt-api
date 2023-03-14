import { ComponentFixture, TestBed } from "@angular/core/testing";

import { SelfActivateComponent } from "./self-activate.component";

describe("SelfActivateComponent", () => {
  let component: SelfActivateComponent;
  let fixture: ComponentFixture<SelfActivateComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SelfActivateComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SelfActivateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
