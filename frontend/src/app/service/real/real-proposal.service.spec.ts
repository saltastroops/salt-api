import { TestBed } from '@angular/core/testing';

import { RealProposalService } from './real-proposal.service';

describe('RealProposalService', () => {
  let service: RealProposalService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(RealProposalService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
