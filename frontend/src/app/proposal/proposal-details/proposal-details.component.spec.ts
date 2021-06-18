import { ProposalDetailsComponent } from './proposal-details.component';
import {render} from '@testing-library/angular';
import {nl2brPipe} from '../../nl2br.pipe';
import {proposal} from '../../mock/proposal-data';

describe('ProposalDetailsComponent', () => {
  const generalProposalInfo = proposal.general_info;
  it('should create', async () => {
    const component = await render(ProposalDetailsComponent, {
      componentProperties: {
        general_proposal_info: generalProposalInfo
      },
      declarations: [nl2brPipe]
    });
    expect(component).toBeTruthy();
  });
});
