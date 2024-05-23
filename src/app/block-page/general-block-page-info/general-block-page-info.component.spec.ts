import { ComponentFixture, TestBed } from '@angular/core/testing';

import { GeneralBlockPageInfoComponent } from './general-block-page-info.component';

describe('BlockProposalGeneralComponent', () => {
  let component: GeneralBlockPageInfoComponent;
  let fixture: ComponentFixture<GeneralBlockPageInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ GeneralBlockPageInfoComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GeneralBlockPageInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
