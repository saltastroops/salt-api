import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ProposalDownloadComponent } from './proposal-download.component';

describe('ProposalDownloadComponent', () => {
  let component: ProposalDownloadComponent;
  let fixture: ComponentFixture<ProposalDownloadComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ ProposalDownloadComponent ]
    })
    .compileComponents();
  });

  beforeEach(() => {
    fixture = TestBed.createComponent(ProposalDownloadComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
