import { ComponentFixture, TestBed } from "@angular/core/testing";

import { InstrumentConfigTableComponent } from "./instrument-config-table.component";

describe("InstrumentConfigTableComponent", () => {
  let component: InstrumentConfigTableComponent;
  let fixture: ComponentFixture<InstrumentConfigTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [InstrumentConfigTableComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(InstrumentConfigTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
