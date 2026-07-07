# Log Report Task

There is an Apache-style access log file at:

`/app/access.log`

Your task is to analyze the log and create a JSON summary report at:

`/app/report.json`

The report must be a valid JSON object.

## Required report fields

The JSON report must include these fields:

```json
{
  "total_requests": 0,
  "unique_ips": 0,
  "status_counts": {},
  "top_path": ""
}