import { TestBed } from '@angular/core/testing';

import { MockBlockService } from './mock-block.service';

describe('BlockService', () => {
  let service: MockBlockService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(MockBlockService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
