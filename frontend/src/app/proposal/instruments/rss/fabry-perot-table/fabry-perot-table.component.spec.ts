import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FabryPerotTableComponent } from './fabry-perot-table.component';

describe('PolarimetryImagingTableComponent', () => {
  let component: FabryPerotTableComponent;
  let fixture: ComponentFixture<FabryPerotTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ FabryPerotTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FabryPerotTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
