import { ComponentFixture, TestBed } from '@angular/core/testing';

import { FabryPerotComponent } from './fabry-perot.component';

describe('PolarimetryImagingTableComponent', () => {
  let component: FabryPerotComponent;
  let fixture: ComponentFixture<FabryPerotComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [FabryPerotComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(FabryPerotComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
