from pytest_mock import MockerFixture

from saltapi.web.schema.proposal import ProposalProgressInput


def test_proposal_progress_validates_values(mocker: MockerFixture) -> None:
    value = "RSA:100"
    mocked_parser = mocker.patch(
        "saltapi.web.schema.proposal.parse_partner_requested_percentages",
        return_value=value,
    )
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
    mocked_parser.assert_called_once_with(value)
    assert ppi.partner_requested_percentages == value
