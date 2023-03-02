from typing import Any, Dict, List, Optional, cast


def _style_rules() -> str:
    return """\
<style>
    body{
        counter-reset: section;
        line-height: 1.2;
    }
    table, th {
        border: 1px solid black;
    }
    table {
        border-collapse: collapse;
        width: 100%;
    }
    td {
        border-right: 1px solid black;
    }
    td, th {
        padding-left: 0.5em;
        padding-right: 0.5em;
    }
    td.number {
        text-align: right;
    }
    table[role="presentation"] {
        width: inherit;
    }
    table[role="presentation"], table[role="presentation"] td {
        border: none;
    }
    table[role="presentation"] td {
        padding: 0 0.5em 0 0;
    }
    .section {
        border: 1px solid black;
        margin-bottom: 1.2em;
    }
    .section > div {
        padding: 0.75em;
    }
    table, tr, td, th, tbody, thead, tfoot, .section {
        page-break-inside: avoid !important;
    }
    .description {
        font-style: italic;
    }
    .label, .important {
        font-weight: bold;
    }
    .has-two-columns {
        display: grid;
        grid-template-columns: 200px 1fr;
    }
    .has-top-margin {
        margin-top: 0.75em;
    }
    .indented {
        margin-left: 1em;
    }
    h1 {
        font-size: 1.5em;
    }
    h2 {
        font-size: 1.1em;
        padding-bottom: 0;
        margin-bottom: 0;
    }
    h2::before {
        counter-increment: section;
        content: counter(section) ". ";
    }
    h3 {
        font-size: 1.05em;
        margin-top: 0.75em;
        margin-bottom: 0.4em;
        padding-top: 0;
    }
    h3:first-of-type {
        margin-top: 0;
    }
    h1, h2 {
        margin-top: 0;
        padding-top: 0;
    }
    .heading {
        border-bottom: 1px solid black;
    }
</style>
"""


def _semester_section(semester: str) -> str:
    return f"""\
<div class="section">
    <div>This report is for semester {semester}.</div>
</div>
"""


def _previous_requests_section(
    previous_requests: List[Dict[str, Any]],
    previous_conditions: Optional[Dict[str, Any]],
) -> str:
    section = f"""\
<div class="section">
    <div class="heading">
        <h2>PREVIOUS REQUESTS, ALLOCATIONS, COMPLETENESS</h2>
        <div class="description">
            This section lists the originally requested times, as well as the allocated
            times and the completion. It also gives the originally requested observing
            conditions.
        </div>
    </div>
    <div>
        <h3>Original time requests, time allocations and completeness</h3>
        <table>
            <tr>
                <th>Semester</th>
                <th>Requested Time</th>
                <th>Allocated Time</th>
                <th>Observed Time</th>
                <th>Completion</th>
            </tr>
"""
    for p in sorted(previous_requests, key=lambda i: cast(str, i["semester"])):
        section += f"""\
            <tr>
                <td>{p['semester']}</td>
                <td class="number">{p['requested_time']} seconds</td>
                <td class="number">{p['allocated_time']} seconds</td>
                <td class="number">{p['observed_time']} seconds</td>
                <td class="number">
                    {str(round((p['observed_time']/p['allocated_time'])*100, 1)) + "%"
                    if p['allocated_time']
                    else 'n/a'}
                </td>
            </tr>
        """
    section += f"""\
        </table>
        <h3>Previously requested observing conditions</h3>
"""
    if previous_conditions:
        section += f"""\
        <table role="presentation">
            <tr>
                <td class="label">Maximum seeing:</td>
                <td>{previous_conditions['seeing']} arcseconds
            </tr>
            <tr>
                <td class="label">Transparency:</td>
                <td>{previous_conditions['transparency']}</td>
            </tr>
        </table>
        <div class="label">Brief description of observing conditions:</div>
        <div class="indented">{previous_conditions['description']}</div>
"""
    else:
        section += """
        <div>
            There is no Phase 1 proposal and hence there are no previously requested
            observing conditions.
        </div>
        """

    section += """\
    </div>
</div>
"""

    return section


def _new_request_section(new_request: Dict[str, Any]) -> str:
    section = f"""\
<div class="section">
    <div class="heading">
        <h2>REQUEST FOR THE NEXT SEMESTER</h2>
        <div class="description">
            This section lists the requests for the next semester.
        </div>
    </div>
    <div>
        <h3>Request for semester {new_request['semester']}</h3>
        <table role="presentation">
            <tr>
                <td class="label">Requested time:</td>
                <td>{new_request['requested_time']} seconds</td>
            </tr>
            <tr>
                <td class="label">Maximum seeing:</td>
                <td>{new_request['maximum_seeing']} arcseconds</td>
            </tr>
            <tr>
                <td class="label">Transparency:</td>
                <td>{new_request['transparency']}</td>
            </tr>
        </table>
        <div class="label has-top-margin">
            Brief description of observing conditions:
        </div>
        <div class="indented">
            {new_request['description_of_observing_constraints']}
        </div>
        <div class="label has-top-margin">
            The following reasons are given for changes from the original requests.
        </div>
        <div class="indented">{new_request['change_reason']}</div>
"""
    if "additional_pdf" in new_request:
        section += """\
        <div class="important has-top-margin">
            A supplementary pdf is attached to this report.
        </div>
"""

    section += """
    </div>
</div>
"""

    return section


def _status_summary_section(new_request: Dict[str, Any]) -> str:
    return f"""\
<div class="section">
    <div class="heading">
        <h2>STATUS SUMMARY</h2>
        <div class="description">
            This section gives a summary of the proposal status.
        </div>
    </div>
    <div>{new_request['summary_of_proposal_status']}</div>
</div>
"""


def _strategy_changes_section(new_request: Dict[str, Any]) -> str:
    return f"""\
<div class="section">
    <div class="heading">
        <h2>STRATEGY CHANGES</h2>
        <div class="description">
            This section outlines how the TAC suggestions regarding a change of strategy
            will be addressed.
        </div>
    </div>
    <div>{new_request['strategy_changes']}</div>
</div>
"""


def create_proposal_progress_html(
    proposal_code: str,
    semester: str,
    previous_requests: List[Dict[str, Any]],
    previous_conditions: Optional[Dict[str, Any]],
    new_request: Dict[str, Any],
) -> str:
    html_content = f"""\
<!DOCTYPE html>
<html lang="en">
    <head>
      <meta charset="UTF-8">
      <title>Progress report for {proposal_code}</title>
    </head>
"""
    html_content += _style_rules()
    html_content += f"""\
    <body>
        <h1>
            Multisemester Proposal Progress Report:<br>
            {proposal_code}
        </h1>
"""
    html_content += _semester_section(semester)
    html_content += _previous_requests_section(previous_requests, previous_conditions)
    html_content += _new_request_section(new_request)
    html_content += _status_summary_section(new_request)
    html_content += _strategy_changes_section(new_request)
    html_content += f"""\
    </body>
</html>
"""

    return html_content
