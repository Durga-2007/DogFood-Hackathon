import sys
sys.path.insert(0, ".")

# Import from run.py directly
import importlib.util
spec = importlib.util.spec_from_file_location("run_module", "run.py")
run = importlib.util.module_from_spec(spec)
spec.loader.exec_module(run)

print("Test 1: GET /projects no auth")
status, body = run.make_request("http://localhost:8080/projects")
print("  status:", status, "body len:", len(body))
print("  Glass Signal:", "Glass Signal" in body)

print("Test 2: parse_auth_header")
h = run.parse_auth_header("Authorization: Bearer prt_token_2e889c0d1e2f3a4b5c6d7e8f9a0b1c2d")
print("  parsed:", h)

print("Test 3: POST submit-new")
status2, body2 = run.make_request(
    "http://localhost:8080/api/projects/submit-new",
    method="POST",
    headers=h,
    body='{"title":"test","event_id":"evt_01"}'
)
print("  status:", status2, "body:", body2[:100])
