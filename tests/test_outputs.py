import json
import re
from collections import Counter
from pathlib import Path


REPORT_PATH = Path("/app/report.json")
LOG_PATH = Path("/app/access.log")

LOG_PATTERN = re.compile(
    r'^(?P<ip>\S+) \S+ \S+ \[[^\]]+\] "(?P<method>\S+) (?P<path>\S+) (?P<protocol>[^"]+)" (?P<status>\d{3}) \S+'
)


def parse_expected_report():
    total_requests = 0
    unique_ips = set()
    status_counts = Counter()
    path_counts = Counter()

    for line in LOG_PATH.read_text(encoding="utf-8").splitlines():
        match = LOG_PATTERN.match(line)
        if not match:
            continue

        total_requests += 1
        unique_ips.add(match.group("ip"))
        status_counts[match.group("status")] += 1
        path_counts[match.group("path")] += 1

    top_path = path_counts.most_common(1)[0][0] if path_counts else None

    return {
        "total_requests": total_requests,
        "unique_ips": len(unique_ips),
        "status_counts": dict(status_counts),
        "top_path": top_path,
    }


def load_report():
    return json.loads(REPORT_PATH.read_text(encoding="utf-8"))


def test_report_file_created():
    """Success criterion: Create the JSON report at /app/report.json."""
    assert REPORT_PATH.exists(), "report.json was not created at /app/report.json"


def test_report_is_valid_json_object():
    """Success criterion: The report must be valid JSON and contain one JSON object."""
    report = load_report()
    assert isinstance(report, dict), "report.json must contain a JSON object"


def test_total_requests_is_correct():
    """Success criterion: total_requests must equal the number of parsed log requests."""
    report = load_report()
    expected = parse_expected_report()
    assert report.get("total_requests") == expected["total_requests"]


def test_unique_ips_is_correct():
    """Success criterion: unique_ips must equal the number of distinct client IP addresses."""
    report = load_report()
    expected = parse_expected_report()
    assert report.get("unique_ips") == expected["unique_ips"]


def test_status_counts_are_correct():
    """Success criterion: status_counts must contain the correct count for each HTTP status code."""
    report = load_report()
    expected = parse_expected_report()
    assert report.get("status_counts") == expected["status_counts"]


def test_top_path_is_correct():
    """Success criterion: top_path must be the most frequently requested path."""
    report = load_report()
    expected = parse_expected_report()
    assert report.get("top_path") == expected["top_path"]