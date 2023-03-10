import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProposalStatusComponent } from './proposal-status.component';

describe('ProposalStatusComponent', () => {
  let component: ProposalStatusComponent;
  let fixture: ComponentFixture<ProposalStatusComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProposalStatusComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProposalStatusComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
