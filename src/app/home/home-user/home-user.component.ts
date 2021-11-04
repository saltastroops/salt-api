import { Component, OnInit } from '@angular/core';
import { ProposalListItem } from '../../types/proposal';
import { ProposalService } from '../../service/proposal.service';
import { currentSemester } from '../../utils';

@Component({
  selector: 'wm-home-user',
  templateUrl: './home-user.component.html',
  styleUrls: ['./home-user.component.scss'],
})
export class HomeUserComponent implements OnInit {
  proposals?: ProposalListItem[];
  selectedSemester: string = currentSemester();

  constructor(private proposalService: ProposalService) {}

  ngOnInit(): void {
    this.proposalService.getProposals().subscribe((p) => (this.proposals = p));
  }

  availableSemesters(): string[] {
    const startYear = 2006;
    const endYear = new Date().getFullYear() + 5;
    const semesters: string[] = [];
    for (let year = startYear; year <= endYear; year++) {
      semesters.push(`${year}-1`, `${year}-2`);
    }
    return semesters;
  }
}
