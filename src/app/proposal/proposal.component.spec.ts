import { TestBed } from '@angular/core/testing';

import { ProposalComponent } from './proposal.component';
import { RouterTestingModule } from '@angular/router/testing';
import { ActivatedRoute } from '@angular/router';
import { render } from '@testing-library/angular';
import { HttpClientTestingModule } from '@angular/common/http/testing';

describe('ProposalComponent', () => {
  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [ProposalComponent],
      imports: [RouterTestingModule],
      providers: [
        {
          provide: ActivatedRoute,
          useValue: { snapshot: { paramMap: { get: () => '2020-2-SCI-043' } } },
        },
      ],
    }).compileComponents();
  });

  it('should create', async () => {
    const component = await render(ProposalComponent, {
      imports: [HttpClientTestingModule],
    });
    expect(component).toBeTruthy();
  });
});
