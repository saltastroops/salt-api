import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MosSlitMaskComponent } from './mos-slit-mask.component';

describe('MosTableComponent', () => {
  let component: MosSlitMaskComponent;
  let fixture: ComponentFixture<MosSlitMaskComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [MosSlitMaskComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(MosSlitMaskComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
