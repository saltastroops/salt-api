import { ComponentFixture, TestBed } from "@angular/core/testing";

import { SalticamConfigRowComponent } from "./salticam-config-row.component";

describe("SalticamConfigRowComponent", () => {
  let component: SalticamConfigRowComponent;
  let fixture: ComponentFixture<SalticamConfigRowComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [SalticamConfigRowComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SalticamConfigRowComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
