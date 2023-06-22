from typing import Any, Dict, List, Optional, cast

from jinja2 import Environment, FileSystemLoader

from saltapi.util import next_semester


def create_proposal_progress_html(
    proposal_code: str,
    semester: str,
    previous_requests: List[Dict[str, Any]],
    previous_conditions: Optional[Dict[str, Any]],
    new_request: Dict[str, Any],
) -> str:
    sorted_previous_requests = sorted(
        previous_requests, key=lambda i: cast(str, i["semester"])
    )
    _next_semester = next_semester(new_request["semester"])

    environment = Environment(loader=FileSystemLoader("saltapi/templates/"))

    template = environment.get_template("proposal_progress.html")

    html = template.render(
        sorted_previous_requests=sorted_previous_requests,
        proposal_code=proposal_code,
        semester=semester,
        previous_requests=previous_requests,
        previous_conditions=previous_conditions,
        _next_semester=_next_semester,
        new_request=new_request,
    )

    return html
