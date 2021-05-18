import { TestBed } from '@angular/core/testing';

import { MockProposalService } from './mock-proposal.service';

describe('MockProposalService', () => {
  let service: MockProposalService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MockProposalService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
