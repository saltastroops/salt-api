import { RealProposalService } from './real-proposal.service';
import { environment } from '../../../environments/environment';
import { proposal } from '../../mock/proposal-data';
import * as camelcaseKeys from 'camelcase-keys';
import { TestBed } from '@angular/core/testing';
import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing';
import { HttpClient } from '@angular/common/http';

describe('RealProposalService', () => {
  let service: RealProposalService;
  let httpClient: HttpClient;
  let httpTestingController: HttpTestingController;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
    });
    httpClient = TestBed.inject(HttpClient);
    httpTestingController = TestBed.inject(HttpTestingController);
    service = TestBed.inject(RealProposalService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should return the content returned by the server', () => {
    const url = environment.apiUrl + '/proposals/2020-1-MLT-005';

    service.getProposal('2020-1-MLT-005').subscribe((data) => {
      const expected = camelcaseKeys(proposal, { deep: true });
      console.log({ data, expected });
      expect(data).toEqual(expected);
    });

    const req = httpTestingController.expectOne(url);
    req.flush(proposal);
  });

  it('should raise an error', () => {
    const url = environment.apiUrl + '/proposals/FAIL-CODE-101';
    const errorMessage = 'The server did not like this request.';

    service.getProposal('FAIL-CODE-101').subscribe(
      () => fail('Should have failed with an error.'),
      (error) => {
        //expect(error).toEqual('The request has failed.');
      }
    );

    const req = httpTestingController.expectOne(url);
    req.flush(errorMessage, { status: 400, statusText: 'Bad Request' });
  });
});
