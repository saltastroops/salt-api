from pytest_mock import MockerFixture

import saltapi
from saltapi.web.schema.proposal import ProposalProgressInput


def test_proposal_progress_validates_values(mocker: MockerFixture) -> None:
    mocker.patch("saltapi.web.schema.proposal.parse_partner_requested_percentages")
    value = "RSA:100"
    ppi = ProposalProgressInput(
        requested_time=3456,
        maximum_seeing=3,
        transparency="Thin cloud",
        description_of_observing_constraints="Any will do",
        change_reason="n/a",
        summary_of_proposal_status="In progress",
        strategy_changes="n/a",
        partner_requested_percentages=value,
    )
    saltapi.web.schema.proposal.parse_partner_requested_percentages.assert_called_once_with(  # noqa
        value
    )
    assert ppi.partner_requested_percentages == value
