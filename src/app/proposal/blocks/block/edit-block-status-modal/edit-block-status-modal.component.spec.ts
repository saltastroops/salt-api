import { ComponentFixture, TestBed } from "@angular/core/testing";

import { EditBlockStatusModalComponent } from "./edit-block-status-modal.component";

describe("EditBlockStatusModalComponent", () => {
  let component: EditBlockStatusModalComponent;
  let fixture: ComponentFixture<EditBlockStatusModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EditBlockStatusModalComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EditBlockStatusModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
