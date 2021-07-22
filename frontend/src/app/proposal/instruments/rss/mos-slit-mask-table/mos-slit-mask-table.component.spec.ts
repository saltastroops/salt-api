import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MosSlitMaskTableComponent } from './mos-slit-mask-table.component';

describe('MosTableComponent', () => {
  let component: MosSlitMaskTableComponent;
  let fixture: ComponentFixture<MosSlitMaskTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ MosSlitMaskTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MosSlitMaskTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
