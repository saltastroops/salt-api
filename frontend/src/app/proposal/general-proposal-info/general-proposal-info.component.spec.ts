import { TestBed } from '@angular/core/testing';
import { GeneralProposalInfoComponent } from './general-proposal-info.component';
import {proposal} from '../../mock/proposal-data';
import {render} from '@testing-library/angular';
import {SummaryOfExecutedObservationsComponent} from '../summary-of-executed-observations/summary-of-executed-observations.component';
import {nl2brPipe} from '../../nl2br.pipe';

describe('GeneralComponent', () => {

  it('should create', async () => {
    const component = await render(GeneralProposalInfoComponent, {
      componentProperties: {
        general_proposal_info: proposal.general_info,
        current_semester: { year: 2020, semester: 1 }
      },
      declarations: [ nl2brPipe ]
    });
    expect(component).toBeTruthy();
  });
});
