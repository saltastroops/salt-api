from pydantic import ValidationError

from saltapi.web.schema.common import ProposalCode
import pytest


@pytest.mark.parametrize("code", ["2021-1-SCI-001", "2022-2-ORP-007", "2023-1-DDT-001"])
def test_valid_proposal_code(code: str):
    assert ProposalCode.validate(code) == code


@pytest.mark.parametrize(
    "invalid_code",
    [
        "20a1-1-ABC-123",  # Invalid year
        "2021-3-ABC-123",  # Invalid semester
        "2021-1-_ABC-123",  # Underscore can't start the letter sequence
        "2021-1-ABC_-123",  # Underscore can't end the letter sequence
        "2021-1-ABC-12",  # Invalid number of digits
    ],
)
def test_invalid_proposal_code(invalid_code: str):
    with pytest.raises(ValueError, match="incorrect proposal code"):
        ProposalCode.validate(invalid_code)


def test_non_string_input():
    with pytest.raises(TypeError, match="string required"):
        ProposalCode.validate(123)
