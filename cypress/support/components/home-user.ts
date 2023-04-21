const PROPOSAL_SEMESTERS = '[data-test="proposal-semester"]';
const START_SEMESTER = '[data-test="start-semester"]';
const END_SEMESTER = '[data-test="end-semester"]';
const APPLY_BUTTON = '[data-test="apply"]';
const SELECT_SEMESTER = '[data-test="select-semester"]';
const INPUT_SEMESTER_ERROR = '[data-test="semester-error"]';

const CURRENT_SEMESTER = '[data-test="current-semester"]';
const CURRENT_AND_NEXT_SEMESTER = '[data-test="current-and-next-semester"]';
const SEMESTER_RANGE = '[data-test="semester-range"]';
const SINGLE_SEMESTER = '[data-test="single-semester"]';

const FILTER_PROPOSALS_REQUIRING_ATTENTION =
  '[data-test="requiring-attention"]';
const FILTER_UNCHECKED_PROPOSALS = '[data-test="unchecked"]';
const FILTER_UNASSIGNED_PROPOSALS = '[data-test="unassigned"]';
const FILTER_ACTIVE_PROPOSALS = '[data-test="active"]';
const FILTER_COMPLETED_PROPOSALS = '[data-test="completed"]';
const FILTER_SCIENCE_PROPOSALS = '[data-test="science"]';
const FILTER_DDT_PROPOSALS = '[data-test="ddt"]';
const FILTER_MY_PROPOSALS = '[data-test="my-proposals"]';
const FILTER_REJECTED_COMPLETED_EXPIRED_PROPOSALS =
  '[data-test="rejected-completed-expired"]';
const FILTER_PHASE1_PROPOSALS = '[data-test="phase1"]';
const FILTER_PHASE2_PROPOSALS = '[data-test="phase2"]';
const FILTER_COMMISSIONING_PROPOSALS = '[data-test="commissioning"]';

const PROPOSAL_TYPES = '[data-test="proposal-type"]';
const PROPOSAL_STATUSES = '[data-test="proposal-status"]';
const PHASES = '[data-test="proposal-phase"]';
const LIAISON_ASTRONOMER = '[data-test="proposal-astronomer"]';
const PRINCIPAL_INVESTIGATOR = '[data-test="proposal-principal-investigator"]';

const PROPOSAL_ROW = '[data-test="proposal-row"]';

const SORT_BY_PROPOSAL_ID_COLUMN = '[data-test="proposal-id-header"]';
const SORT_BY_PROPOSAL_CODE_COLUMN = '[data-test="proposal-code-header"]';
const SORT_BY_PROPOSAL_TITLE_COLUMN = '[data-test="proposal-title-header"]';
const SORT_BY_PROPOSAL_SEMESTER_COLUMN =
  '[data-test="proposal-semester-header"]';
const SORT_BY_PROPOSAL_PHASE_COLUMN = '[data-test="proposal-phase-header"]';
const SORT_BY_PROPOSAL_STATUS_COLUMN = '[data-test="proposal-status-header"]';
const SORT_BY_PROPOSAL_TYPE_COLUMN = '[data-test="proposal-type-header"]';
const SORT_BY_PROPOSAL_ASTRONOMER_COLUMN =
  '[data-test="proposal-astronomer-header"]';

export class HomeUser {
  static proposalsListEmpty(): void {
    cy.get(PROPOSAL_ROW).should("not.exist");
  }

  static clickCurrentSemesterRadioButton(): void {
    cy.get(CURRENT_SEMESTER).click();
  }

  static currentSemesterRadioButtonChecked(checked: boolean): void {
    if (checked) {
      cy.get(CURRENT_SEMESTER).should("be.checked");
    } else {
      cy.get(CURRENT_SEMESTER).should("not.be.checked");
    }
  }

  static clickCurrentAndNextSemesterRadioButton(): void {
    cy.get(CURRENT_AND_NEXT_SEMESTER).click();
  }

  static currentAndNextSemesterRadioButtonChecked(checked: boolean): void {
    if (checked) {
      cy.get(CURRENT_AND_NEXT_SEMESTER).should("be.checked");
    } else {
      cy.get(CURRENT_AND_NEXT_SEMESTER).should("not.be.checked");
    }
  }

  static clickSemesterRangeRadioButton(): void {
    cy.get(SEMESTER_RANGE).click();
  }

  static semesterRangeRadioButtonChecked(checked: boolean): void {
    if (checked) {
      cy.get(SEMESTER_RANGE).should("be.checked");
    } else {
      cy.get(SEMESTER_RANGE).should("not.be.checked");
    }
  }

  static clickSingleSemesterRadioButton(): void {
    cy.get(SINGLE_SEMESTER).click();
  }

  static singleSemesterRadioButtonChecked(checked: boolean): void {
    if (checked) {
      cy.get(SINGLE_SEMESTER).should("be.checked");
    } else {
      cy.get(SINGLE_SEMESTER).should("not.be.checked");
    }
  }

  static typeSemesterRanges(
    start_semester: string,
    end_semester: string,
  ): void {
    if (start_semester != "") {
      cy.get(START_SEMESTER).type(start_semester);
    }
    if (end_semester != "") {
      cy.get(END_SEMESTER).type(end_semester);
    }
  }

  static noInputSemesterError(): void {
    cy.get(INPUT_SEMESTER_ERROR).then((text) => {
      const error_message = text.text();
      error_message.includes(
        "Please provide a start and/or end semester in the format yyyy-n",
      );
    });
  }

  static wrongInputSemesterError(semester: string): void {
    cy.get(INPUT_SEMESTER_ERROR).then((text) => {
      const error_message = text.text();
      error_message.includes(
        `The semester: ${semester} must be of the form yyyy-n`,
      );
    });
  }

  static clickApplyButton(): void {
    cy.get(APPLY_BUTTON).click();
  }

  static selectSemester(semester: string): void {
    cy.get(SELECT_SEMESTER).select(semester);
  }

  static filteredBySingleSemester(expected_semester: string): void {
    cy.get(PROPOSAL_SEMESTERS).each(($el) => {
      const semester = $el.text();
      expect(semester).to.equal(expected_semester);
    });
  }

  static filteredByCurrentAndNextSemester(): void {
    const semesters = [];
    cy.get(PROPOSAL_SEMESTERS)
      .each(($el) => {
        const semester = $el.text();
        semesters.push(semester);
      })
      .then(() => {
        const current_and_next_semesters = Array.from(new Set(semesters));
        expect(current_and_next_semesters.length == 2);
        semesters.forEach((semester) =>
          expect(semester).to.be.oneOf(current_and_next_semesters),
        );
      });
  }

  static filteredBySemesterRange(
    start_semester: string,
    end_semester: string,
  ): void {
    const semesters = [];
    cy.get(PROPOSAL_SEMESTERS)
      .each(($el) => {
        const semester = $el.text();
        semesters.push(semester);
      })
      .then(() => {
        expect(Array.from(new Set(semesters)).length > 1).to.be.true;

        semesters.forEach((semester) => {
          if (start_semester != "" && end_semester != "") {
            expect(semester >= start_semester).to.be.true;
            expect(semester <= end_semester).to.be.true;
          } else if (start_semester == "") {
            expect(semester <= end_semester).to.be.true;
          } else {
            expect(semester >= start_semester).to.be.true;
          }
        });
      });
  }

  static semesterRangeInputsDisabled(disabled: boolean): void {
    if (disabled) {
      cy.get(START_SEMESTER).should("be.disabled");
      cy.get(END_SEMESTER).should("be.disabled");
      cy.get(APPLY_BUTTON).should("be.disabled");
    } else {
      cy.get(START_SEMESTER).should("not.be.disabled");
      cy.get(END_SEMESTER).should("not.be.disabled");
      cy.get(APPLY_BUTTON).should("not.be.disabled");
    }
  }

  static semesterSelectDisabled(disabled: boolean): void {
    if (disabled) {
      cy.get(SELECT_SEMESTER).should("be.disabled");
    } else {
      cy.get(SELECT_SEMESTER).should("not.be.disabled");
    }
  }

  static clickRequiringAttentionCheckbox(): void {
    cy.get(FILTER_PROPOSALS_REQUIRING_ATTENTION).click();
  }

  static requiringAttentionFilterCheckboxChecked(checked: boolean): void {
    if (checked) {
      cy.get(FILTER_PROPOSALS_REQUIRING_ATTENTION).should("be.checked");
    } else {
      cy.get(FILTER_PROPOSALS_REQUIRING_ATTENTION).should("not.be.checked");
    }
  }

  static clickUnassignedCheckbox(): void {
    cy.get(FILTER_UNASSIGNED_PROPOSALS).click();
  }

  static unassignedFilterCheckboxChecked(checked: boolean): void {
    if (checked) {
      cy.get(FILTER_UNASSIGNED_PROPOSALS).should("be.checked");
    } else {
      cy.get(FILTER_UNASSIGNED_PROPOSALS).should("not.be.checked");
    }
  }

  static clickUncheckedCheckbox(): void {
    cy.get(FILTER_UNCHECKED_PROPOSALS).click();
  }

  static uncheckedFilterCheckboxChecked(checked: boolean): void {
    if (checked) {
      cy.get(FILTER_UNCHECKED_PROPOSALS).should("be.checked");
    } else {
      cy.get(FILTER_UNCHECKED_PROPOSALS).should("not.be.checked");
    }
  }

  static clickActiveCheckbox(): void {
    cy.get(FILTER_ACTIVE_PROPOSALS).click();
  }

  static activeFilterCheckboxChecked(checked: boolean): void {
    if (checked) {
      cy.get(FILTER_ACTIVE_PROPOSALS).should("be.checked");
    } else {
      cy.get(FILTER_ACTIVE_PROPOSALS).should("not.be.checked");
    }
  }

  static clickCommissioningCheckbox(): void {
    cy.get(FILTER_COMMISSIONING_PROPOSALS).click();
  }

  static commissioningFilterCheckboxChecked(checked: boolean): void {
    if (checked) {
      cy.get(FILTER_COMMISSIONING_PROPOSALS).should("be.checked");
    } else {
      cy.get(FILTER_COMMISSIONING_PROPOSALS).should("not.be.checked");
    }
  }

  static clickCompletedCheckbox(): void {
    cy.get(FILTER_COMPLETED_PROPOSALS).click();
  }

  static completedFilterCheckboxChecked(checked: boolean): void {
    if (checked) {
      cy.get(FILTER_COMPLETED_PROPOSALS).should("be.checked");
    } else {
      cy.get(FILTER_COMPLETED_PROPOSALS).should("not.be.checked");
    }
  }

  static clickScienceCheckbox(): void {
    cy.get(FILTER_SCIENCE_PROPOSALS).click();
  }

  static scienceFilterCheckboxChecked(checked: boolean): void {
    if (checked) {
      cy.get(FILTER_SCIENCE_PROPOSALS).should("be.checked");
    } else {
      cy.get(FILTER_SCIENCE_PROPOSALS).should("not.be.checked");
    }
  }

  static clickDDTCheckbox(): void {
    cy.get(FILTER_DDT_PROPOSALS).click();
  }

  static ddtFilterCheckboxChecked(checked: boolean): void {
    if (checked) {
      cy.get(FILTER_DDT_PROPOSALS).should("be.checked");
    } else {
      cy.get(FILTER_DDT_PROPOSALS).should("not.be.checked");
    }
  }

  static clickMyProposalsCheckbox(): void {
    cy.get(FILTER_MY_PROPOSALS).click();
  }

  static myProposalsFilterCheckboxChecked(checked: boolean): void {
    if (checked) {
      cy.get(FILTER_MY_PROPOSALS).should("be.checked");
    } else {
      cy.get(FILTER_MY_PROPOSALS).should("not.be.checked");
    }
  }

  static clickPhase1Checkbox(): void {
    cy.get(FILTER_PHASE1_PROPOSALS).click();
  }

  static phase1FilterCheckboxChecked(checked: boolean): void {
    if (checked) {
      cy.get(FILTER_PHASE1_PROPOSALS).should("be.checked");
    } else {
      cy.get(FILTER_PHASE1_PROPOSALS).should("not.be.checked");
    }
  }

  static clickPhase2Checkbox(): void {
    cy.get(FILTER_PHASE2_PROPOSALS).click();
  }

  static phase2FilterCheckboxChecked(checked: boolean): void {
    if (checked) {
      cy.get(FILTER_PHASE2_PROPOSALS).should("be.checked");
    } else {
      cy.get(FILTER_PHASE2_PROPOSALS).should("not.be.checked");
    }
  }

  static clickRejectedCompletedExpiredCheckbox(): void {
    cy.get(FILTER_REJECTED_COMPLETED_EXPIRED_PROPOSALS).click();
  }

  static RejectedCompletedExpiredFilterCheckboxChecked(checked: boolean): void {
    if (checked) {
      cy.get(FILTER_REJECTED_COMPLETED_EXPIRED_PROPOSALS).should("be.checked");
    } else {
      cy.get(FILTER_REJECTED_COMPLETED_EXPIRED_PROPOSALS).should(
        "not.be.checked",
      );
    }
  }

  static filteredProposalsRequiringAttention(username: string): void {
    cy.task("getUser", username).then((user) => {
      cy.get(LIAISON_ASTRONOMER).each(($el) => {
        const astronomer = $el.text();
        expect(astronomer).to.equal(user["givenName"]);
      });

      cy.get(PROPOSAL_STATUSES).each(($el) => {
        const proposal_status = $el.text();
        expect(proposal_status).to.be.oneOf([
          "Under scientific review",
          "Under technical review",
        ]);
      });
    });
  }

  static filteredUncheckedProposals(): void {
    cy.get(PROPOSAL_STATUSES).each(($el) => {
      const status = $el.text();
      expect(status).to.be.oneOf([
        "Under technical review",
        "Under scientific review",
      ]);
    });
  }

  static filteredUnassignedProposals(): void {
    cy.get(LIAISON_ASTRONOMER).each(($el) => {
      const astronomer = $el.text();
      expect(astronomer).to.be.empty;
    });
  }

  static filteredActiveProposals(): void {
    cy.get(PROPOSAL_STATUSES).each(($el) => {
      const status = $el.text();
      expect(status).to.equal("Active");
    });
  }

  static filteredCompletedProposals(): void {
    cy.get(PROPOSAL_STATUSES).each(($el) => {
      const status = $el.text();
      expect(status).to.equal("Completed");
    });
  }

  static filteredScienceProposals(): void {
    cy.get(PROPOSAL_TYPES).each(($el) => {
      const proposal_type = $el.text();
      expect(proposal_type).to.equal("Science");
    });
  }

  static filteredCommissioningProposals(): void {
    cy.get(PROPOSAL_TYPES).each(($el) => {
      const proposal_type = $el.text();
      expect(proposal_type).to.equal("Commissioning");
    });
  }

  static filteredDDTProposals(): void {
    cy.get(PROPOSAL_TYPES).each(($el) => {
      const proposal_type = $el.text();
      expect(proposal_type).to.equal("Director's Discretionary Time");
    });
  }

  static filteredRejectedCompletedExpiredProposals(): void {
    cy.get(PROPOSAL_STATUSES).each(($el) => {
      const proposal_status = $el.text();
      expect(proposal_status).to.be.oneOf(["Rejected", "Completed", "Expired"]);
    });
  }

  static filteredPhase1Proposals(): void {
    cy.get(PHASES).each(($el) => {
      const phase = $el.text();
      expect(phase).to.equal("1");
    });
  }

  static filteredPhase2Proposals(): void {
    cy.get(PHASES).each(($el) => {
      const phase = $el.text();
      expect(phase).to.equal("2");
    });
  }

  static filteredMyProposals(proposalCodes: string[]): void {
    cy.get("[data-test=proposal-code]").each(($el, index) => {
      const proposalCode = $el.text().trim();
      cy.wrap(proposalCode).should("equal", proposalCodes[index]);
    });
  }

  static clickProposalIdColumn(): void {
    cy.get(SORT_BY_PROPOSAL_ID_COLUMN).click();
  }

  static clickProposalCodeColumn(): void {
    cy.get(SORT_BY_PROPOSAL_CODE_COLUMN).click();
  }

  static clickProposalTitleColumn(): void {
    cy.get(SORT_BY_PROPOSAL_TITLE_COLUMN).click();
  }

  static clickProposalSemesterColumn(): void {
    cy.get(SORT_BY_PROPOSAL_SEMESTER_COLUMN).click();
  }

  static clickProposalPhaseColumn(): void {
    cy.get(SORT_BY_PROPOSAL_PHASE_COLUMN).click();
  }

  static clickProposalStatusColumn(): void {
    cy.get(SORT_BY_PROPOSAL_STATUS_COLUMN).click();
  }

  static clickProposalTypeColumn(): void {
    cy.get(SORT_BY_PROPOSAL_TYPE_COLUMN).click();
  }

  static clickProposalAstronomerColumn(): void {
    cy.get(SORT_BY_PROPOSAL_ASTRONOMER_COLUMN).click();
  }

  static proposalsSortedBy(
    column: string,
    order: "ascending" | "descending",
  ): void {
    const valueElement = "[data-test=proposal-" + column + "]";
    const headerElement = "[data-test=proposal-" + column + "-header" + "]";
    const values = [];
    if (order === "ascending") {
      cy.get(headerElement).should("have.class", "asc");
      cy.get(valueElement)
        .each(($el, index) => {
          values[index] = $el.text();
        })
        .then(() => {
          expect(values).to.deep.equal(values.sort());
        });
    }
    if (order === "descending") {
      cy.get(headerElement).should("have.class", "desc");
      cy.get(valueElement)
        .each(($el, index) => {
          values[index] = $el.text();
        })
        .then(() => {
          expect(values).to.deep.equal(values.reverse());
        });
    }
  }
}
