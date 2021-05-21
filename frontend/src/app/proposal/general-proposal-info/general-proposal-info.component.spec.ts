import { ComponentFixture, TestBed } from '@angular/core/testing';
import { GeneralProposalInfoComponent } from './general-proposal-info.component';

describe('GeneralComponent', () => {
  let component: GeneralProposalInfoComponent;
  let fixture: ComponentFixture<GeneralProposalInfoComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [GeneralProposalInfoComponent],
    }).compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(GeneralProposalInfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
