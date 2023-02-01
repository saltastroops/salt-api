import { ComponentFixture, TestBed } from "@angular/core/testing";

import { EditProprietaryPeriodModalComponent } from "./edit-proprietary-period-modal.component";

describe("EditProprietaryPeriodModalComponent", () => {
  let component: EditProprietaryPeriodModalComponent;
  let fixture: ComponentFixture<EditProprietaryPeriodModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EditProprietaryPeriodModalComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EditProprietaryPeriodModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
