import { ComponentFixture, TestBed } from '@angular/core/testing';

import { SlitMaskTableComponent } from './slit-mask-table.component';

describe('SlitMaskComponent', () => {
  let component: SlitMaskTableComponent;
  let fixture: ComponentFixture<SlitMaskTableComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ SlitMaskTableComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(SlitMaskTableComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
