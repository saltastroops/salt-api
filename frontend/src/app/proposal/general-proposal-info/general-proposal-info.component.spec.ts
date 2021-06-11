import { ComponentFixture, TestBed } from '@angular/core/testing';
import { GeneralProposalInfoComponent } from './general-proposal-info.component';
import { GeneralProposalInfo, Semester } from '../../types';
import {proposal} from "../../mock/proposal-data";
import {render} from "@testing-library/angular";

describe('GeneralComponent', () => {
  let component: GeneralProposalInfoComponent;


  it('should create', async () => {
    await render(GeneralProposalInfoComponent, {
      componentProperties: {
        general_proposal_info: proposal.general_info,
        current_semester: { year: 2020, semester: 1 }
      }
    });
    expect(component).toBeTruthy();
  });
});
