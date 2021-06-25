import { GeneralProposalInfoComponent } from './general-proposal-info.component';
import {proposal} from '../../mock/proposal-data';
import {render} from '@testing-library/angular';
import {nl2brPipe} from '../../nl2br.pipe';

describe('GeneralComponent', () => {

  it('should create', async () => {
    const component = await render(GeneralProposalInfoComponent, {
      componentProperties: {
        generalProposalInfo: proposal.general_info,
        currentSemester: { year: 2020, semester: 1 }
      },
      declarations: [ nl2brPipe ]
    });
    expect(component).toBeTruthy();
  });
});
