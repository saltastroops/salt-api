import { ComponentFixture, TestBed } from "@angular/core/testing";

import { MosLegendComponent } from "./mos-legend.component";

describe("LegendComponent", () => {
  let component: MosLegendComponent;
  let fixture: ComponentFixture<MosLegendComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MosLegendComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MosLegendComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it("should create", () => {
    expect(component).toBeTruthy();
  });
});
