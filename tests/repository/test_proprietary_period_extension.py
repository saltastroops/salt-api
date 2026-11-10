from datetime import date, datetime

from sqlalchemy import create_engine

from saltapi.repository.proposal_repository import ProposalRepository


def test_proposals_requesting_more_time_returns_latest_with_history() -> None:
    engine = create_engine("sqlite://")
    with engine.connect() as connection:
        connection.connection.driver_connection.create_function(
            "CONCAT", 2, lambda first, second: f"{first}{second}"
        )
        connection.exec_driver_sql(
            """
            CREATE TABLE ProprietaryPeriodExtensionRequest (
                ProprietaryPeriodExtensionRequest_Id INTEGER PRIMARY KEY,
                ProposalCode_Id INTEGER,
                Reason TEXT,
                MadeAt DATETIME,
                RequestedBy INTEGER,
                RequestedPeriod INTEGER
            )
            """
        )
        connection.exec_driver_sql(
            """
            CREATE TABLE ProprietaryPeriodExtensionDecision (
                ProprietaryPeriodExtensionRequest_Id INTEGER,
                Reason TEXT,
                GrantedPeriod INTEGER
            )
            """
        )
        connection.exec_driver_sql(
            "CREATE TABLE ProposalCode (ProposalCode_Id INTEGER, Proposal_Code TEXT)"
        )
        connection.exec_driver_sql(
            "CREATE TABLE PiptUser (PiptUser_Id INTEGER, Investigator_Id INTEGER)"
        )
        connection.exec_driver_sql(
            """
            CREATE TABLE Investigator (
                Investigator_Id INTEGER,
                FirstName TEXT,
                Surname TEXT,
                Email TEXT
            )
            """
        )
        connection.exec_driver_sql(
            """
            CREATE TABLE ProposalGeneralInfo (
                ProposalCode_Id INTEGER,
                ProprietaryPeriod INTEGER
            )
            """
        )
        connection.exec_driver_sql(
            "INSERT INTO ProposalCode VALUES (1, 'P-1'), (2, 'P-2'), (3, 'P-3'), (4, 'P-4')"
        )
        connection.exec_driver_sql("INSERT INTO PiptUser VALUES (10, 100)")
        connection.exec_driver_sql(
            "INSERT INTO Investigator VALUES (100, 'Ada', 'Lovelace', 'ada@example.com')"
        )
        connection.exec_driver_sql(
            "INSERT INTO ProposalGeneralInfo VALUES (1, 24), (2, 12), (3, 18), (4, 6)"
        )
        connection.exec_driver_sql(
            """
            INSERT INTO ProprietaryPeriodExtensionRequest VALUES
                (1, 1, 'Older request', '2025-01-01 09:00:00', 10, 12),
                (2, 1, 'Latest timestamp tie, lower id', '2026-02-01 09:00:00', 10, 24),
                (3, 1, 'Latest request', '2026-02-01 09:00:00', 10, 36),
                (4, 2, 'Only recent request', '2026-03-01 09:00:00', 10, 18),
                (5, 2, 'Older request', '2025-01-01 09:00:00', 10, 6),
                (6, 3, 'No history', '2026-04-01 09:00:00', 10, 24),
                (7, 4, 'Proposal too old', '2025-01-01 09:00:00', 10, 12)
            """
        )
        connection.exec_driver_sql(
            "INSERT INTO ProprietaryPeriodExtensionDecision VALUES (1, 'Earlier grant', 12), (3, 'Latest grant', 36)"
        )

        repository = ProposalRepository(connection)
        release_date_calls = []

        def get_release_date(period: int, proposal_code: str) -> date:
            release_date_calls.append(proposal_code)
            return date(2030, 1, 1)

        repository.get_release_date = get_release_date
        requests = repository.proprietary_period_extension_requests(
            datetime(2026, 1, 1)
        )

    assert [request["proposal_code"] for request in requests] == ["P-3", "P-2", "P-1"]
    assert [request["id"] for request in requests] == [6, 4, 3]
    assert requests[0]["previous_requests"] == []
    assert requests[0]["current_request"]["request_motivation"] == "No history"
    assert requests[1]["current_request"]["request_motivation"] == "Only recent request"
    assert requests[1]["previous_requests"][0]["made_at"] == "2025-01-01 09:00:00"
    assert requests[1]["previous_requests"][0]["request_motivation"] == "Older request"
    assert requests[1]["granted_period"] is None
    assert requests[2]["current_request"]["request_motivation"] == "Latest request"
    assert requests[2]["previous_requests"][0]["request_motivation"] == (
        "Latest timestamp tie, lower id"
    )
    assert requests[2]["previous_requests"][1]["request_motivation"] == "Older request"
    assert requests[2]["grant_reason"] == "Latest grant"
    assert requests[2]["granted_period"] == 36
    assert requests[2]["current_request"]["requested_period"] == 36
    assert all(request["release_date"] == date(2030, 1, 1) for request in requests)
    assert release_date_calls == ["P-3", "P-2", "P-1"]