#!/usr/bin/env python3
"""
DOGFOOD 2026 acceptance checker.
Usage: python3 run.py .dogfood.toml > acceptance-report.txt

Implements the exact seven checks specified at https://dogfoodhack.com/spec
Standard library only.
"""
import sys
import json
import urllib.request
import urllib.error
import urllib.parse
import os

def load_toml(path):
    """Minimal TOML parser for the .dogfood.toml format."""
    result = {}
    section = None
    with open(path, "r") as f:
        for raw in f:
            line = raw.strip()
            if not line or line.startswith("#"):
                continue
            if line.startswith("[") and line.endswith("]"):
                section = line[1:-1].strip()
                result[section] = {}
                continue
            if "=" in line and section is not None:
                key, _, val = line.partition("=")
                key = key.strip()
                val = val.strip()
                # Strip surrounding quotes
                if (val.startswith('"') and val.endswith('"')) or \
                   (val.startswith("'") and val.endswith("'")):
                    val = val[1:-1]
                # Handle arrays like ["T1", "T2"]
                elif val.startswith("[") and val.endswith("]"):
                    inner = val[1:-1]
                    val = [v.strip().strip('"').strip("'") for v in inner.split(",") if v.strip()]
                result[section][key] = val
    return result

def load_fixture_titles(toml_dir):
    """Load known project titles from fixtures.json (next to run.py or in data/)."""
    candidates = [
        os.path.join(toml_dir, "fixtures.json"),
        os.path.join(toml_dir, "data", "fixtures.json"),
        "fixtures.json",
        os.path.join(os.path.dirname(__file__), "fixtures.json"),
        os.path.join(os.path.dirname(__file__), "data", "fixtures.json"),
    ]
    for path in candidates:
        if os.path.exists(path):
            with open(path, "r") as f:
                data = json.load(f)
            return [p.get("title", "") for p in data.get("projects", [])]
    return []

def make_request(url, method="GET", headers=None, body=None):
    """Make HTTP request, return (status_code, body_text)."""
    req = urllib.request.Request(url, method=method)
    if headers:
        for k, v in headers.items():
            req.add_header(k, v)
    if body:
        req.data = body.encode("utf-8")
        req.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return resp.status, resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")
    except Exception as e:
        return 0, str(e)

def parse_auth_header(header_str):
    """Parse 'HeaderName: Value' into dict."""
    if ":" in header_str:
        name, _, value = header_str.partition(":")
        return {name.strip(): value.strip()}
    return {}

def fmt_pass(label, width=38):
    dots = "." * (width - len(label))
    return f"{label} {dots} PASS"

def fmt_fail(label, detail, width=38):
    dots = "." * (width - len(label))
    return f"{label} {dots} FAIL\n  {detail}"

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 run.py .dogfood.toml")
        sys.exit(1)

    toml_path = sys.argv[1]
    toml_dir = os.path.dirname(os.path.abspath(toml_path))

    cfg = load_toml(toml_path)
    base_url = cfg.get("portal", {}).get("base_url", "http://localhost:8080").rstrip("/")
    claimed = cfg.get("tiers", {}).get("claimed", [])
    if isinstance(claimed, str):
        claimed = [claimed]

    routes = cfg.get("routes", {})
    auth = cfg.get("auth", {})

    gallery_path = routes.get("gallery", "/projects")
    submit_path = routes.get("submit", "/api/projects/submit-new")
    judge_scores_path = routes.get("judge_scores", "/api/judge/scores")
    peer_scores_path = routes.get("peer_scores", "/api/judge/scores?judge=judge_a")
    csv_export_path = cfg.get("routes", {}).get("csv_export", "/api/export.csv")

    auth_organizer = parse_auth_header(auth.get("organizer", ""))
    auth_judge_a = parse_auth_header(auth.get("judge_a", ""))
    auth_judge_b = parse_auth_header(auth.get("judge_b", ""))
    auth_participant = parse_auth_header(auth.get("participant", ""))

    fixture_titles = load_fixture_titles(toml_dir)

    lines = []
    lines.append(f"DOGFOOD 2026 acceptance report")
    lines.append(f"portal:   {base_url}")
    lines.append(f"claimed:  {' '.join(claimed)}")
    lines.append(f"fixtures: {len(fixture_titles)} project titles loaded")
    lines.append("")

    verified = []
    failed = []

    # ── T1 checks ──────────────────────────────────────────────────────────────

    # T1.1 · A stranger can browse the gallery.
    # GET {routes.gallery} no auth header expect 200
    gallery_url = base_url + gallery_path
    status, body = make_request(gallery_url)
    if status == 200:
        lines.append(fmt_pass("T1 gallery is public"))
        verified.append("T1")
    else:
        detail = (f"GET {gallery_url} with no auth\n"
                  f"  got {status}, wanted 200")
        lines.append(fmt_fail("T1 gallery is public", detail))
        failed.append("T1-gallery-public")

    # T1.2 · The gallery shows fixture projects.
    # GET {routes.gallery} expect a known fixture title in the body
    status2, body2 = make_request(gallery_url)
    found_title = None
    for title in fixture_titles:
        if title and title in body2:
            found_title = title
            break
    if found_title:
        lines.append(fmt_pass("T1 project from fixtures shown"))
    else:
        sample = fixture_titles[:3] if fixture_titles else ["(none loaded)"]
        detail = (f"GET {gallery_url}\n"
                  f"  wanted one of: {sample!r}\n"
                  f"  none found in response body")
        lines.append(fmt_fail("T1 project from fixtures shown", detail))
        failed.append("T1-fixture-title")

    # T1.3 · A closed event refuses submissions.
    # POST {routes.submit} as participant expect 4xx
    submit_url = base_url + submit_path
    status3, body3 = make_request(
        submit_url, method="POST",
        headers=auth_participant,
        body='{"title":"Checker submission","event_id":"evt_01"}'
    )
    if 400 <= status3 <= 499:
        lines.append(fmt_pass("T1 closed event refuses submissions"))
    else:
        detail = (f"POST {submit_url} sent as participant\n"
                  f"  got {status3}, wanted 4xx\n"
                  f"  the backend did not enforce the submission deadline")
        lines.append(fmt_fail("T1 closed event refuses submissions", detail))
        failed.append("T1-deadline")

    lines.append("")

    # ── T2 checks ──────────────────────────────────────────────────────────────

    # T2.1 · A judge can read their own scores.
    # GET {routes.judge_scores} as judge_a expect 200
    scores_url = base_url + judge_scores_path
    status4, body4 = make_request(scores_url, headers=auth_judge_a)
    if status4 == 200:
        lines.append(fmt_pass("T2 judge sees own scores"))
        if "T2" not in verified:
            verified.append("T2")
    else:
        detail = (f"GET {scores_url} sent as judge_a\n"
                  f"  got {status4}, wanted 200")
        lines.append(fmt_fail("T2 judge sees own scores", detail))
        failed.append("T2-judge-own-scores")

    # T2.2 · A judge cannot read a peer's scores.
    # GET {routes.peer_scores} as judge_b expect 401 or 403
    peer_url = base_url + peer_scores_path
    status5, body5 = make_request(peer_url, headers=auth_judge_b)
    if status5 in (401, 403):
        lines.append(fmt_pass("T2 judge cannot see peer scores"))
    else:
        detail = (f"GET {peer_url} sent as judge_b; this is the url that returns judge_a's scores\n"
                  f"  got {status5}, wanted 401 or 403\n"
                  f"  the backend returned another judge's scores")
        lines.append(fmt_fail("T2 judge cannot see peer scores", detail))
        failed.append("T2-peer-scores")

    # T2.3 · A participant is not a judge.
    # GET {routes.judge_scores} as participant expect 401 or 403
    status6, body6 = make_request(scores_url, headers=auth_participant)
    if status6 in (401, 403):
        lines.append(fmt_pass("T2 participant blocked"))
    else:
        detail = (f"GET {scores_url} sent as participant\n"
                  f"  got {status6}, wanted 401 or 403")
        lines.append(fmt_fail("T2 participant blocked", detail))
        failed.append("T2-participant-blocked")

    # T2.4 · An organizer can export CSV.
    # GET {routes.csv_export} as organizer expect 200 and a CSV body
    csv_url = base_url + csv_export_path
    status7, body7 = make_request(csv_url, headers=auth_organizer)
    is_csv = (status7 == 200 and ("," in body7 or "\n" in body7))
    if is_csv:
        lines.append(fmt_pass("T2 csv export works"))
    else:
        detail = (f"GET {csv_url} sent as organizer\n"
                  f"  got {status7}, wanted 200 with CSV body")
        lines.append(fmt_fail("T2 csv export works", detail))
        failed.append("T2-csv-export")

    lines.append("")

    # ── Summary ────────────────────────────────────────────────────────────────
    t1_checks = ["T1-gallery-public", "T1-fixture-title", "T1-deadline"]
    t1_passed = not any(f in failed for f in t1_checks)
    t2_checks = ["T2-judge-own-scores", "T2-peer-scores", "T2-participant-blocked", "T2-csv-export"]
    t2_passed = not any(f in failed for f in t2_checks)

    actual_verified = []
    if t1_passed:
        actual_verified.append("T1")
    if t2_passed and "T2" in claimed:
        actual_verified.append("T2")

    lines.append(f"claimed {' '.join(claimed)}, verified {' '.join(actual_verified) or '(none)'}")
    if set(claimed) - set(actual_verified):
        missing = set(claimed) - set(actual_verified)
        lines.append(f"note: claimed but not verified: {' '.join(sorted(missing))}")

    print("\n".join(lines))

if __name__ == "__main__":
    main()
