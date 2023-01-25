import { ComponentFixture, TestBed } from "@angular/core/testing";

import { P1ConfigurationsComponent } from "./p1-configurations.component";

describe("PhaseOneConfigurationsComponent", () => {
  let component: P1ConfigurationsComponent;
  let fixture: ComponentFixture<P1ConfigurationsComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [P1ConfigurationsComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(P1ConfigurationsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
