import { ComponentFixture, TestBed } from "@angular/core/testing";

import { EditBlockVisitStatusModalComponent } from "./edit-block-visit-status-modal.component";

describe("EditBlockVisitStatusModalComponent", () => {
  let component: EditBlockVisitStatusModalComponent;
  let fixture: ComponentFixture<EditBlockVisitStatusModalComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [EditBlockVisitStatusModalComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(EditBlockVisitStatusModalComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
