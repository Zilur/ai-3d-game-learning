"""One-time cleanup for two specifically authorized, fully merged course branches.
Never deletes main. Lease protects against a concurrent branch update.
"""
from __future__ import annotations
import base64
import os
import re
import subprocess

BRANCHES = ("course/foundation-v1", "course/interactive-mastery-v2")

def run(args: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, env=env, text=True, capture_output=True, timeout=60)

def main() -> None:
    if os.environ.get("GITHUB_REF") != "refs/heads/main" or os.environ.get("GITHUB_EVENT_NAME") != "push":
        raise RuntimeError("Cleanup only allowed on a main push")
    if os.environ.get("COURSE_CLEANUP_APPROVED") != "1":
        raise RuntimeError("One-time consolidation gate not satisfied")
    token = os.environ["GH_TOKEN"]
    env = os.environ.copy()
    # Command-scoped credentials: not stored in .git/config and never printed.
    env["GIT_CONFIG_COUNT"] = "1"
    env["GIT_CONFIG_KEY_0"] = "http.https://github.com/.extraheader"
    env["GIT_CONFIG_VALUE_0"] = "AUTHORIZATION: basic " + base64.b64encode(("x-access-token:" + token).encode()).decode()
    for variable in ("GIT_TRACE", "GIT_TRACE_CURL", "GIT_CURL_VERBOSE"):
        env.pop(variable, None)
    for branch in BRANCHES:
        ref = "refs/heads/" + branch
        listed = run(["git", "ls-remote", "--heads", "origin", ref], env)
        if listed.returncode:
            raise RuntimeError("Cannot read remote refs; no cleanup attempted")
        if not listed.stdout.strip():
            print("Already absent: " + branch)
            continue
        fields = listed.stdout.strip().split()
        if len(fields) != 2 or fields[1] != ref or not re.fullmatch(r"[0-9a-f]{40}", fields[0]):
            raise RuntimeError("Unexpected remote ref response")
        sha = fields[0]
        ancestor = run(["git", "merge-base", "--is-ancestor", sha, "HEAD"], env)
        if ancestor.returncode:
            print("SKIPPED, branch has content not proven merged: " + branch)
            continue
        deleted = run(["git", "push", "--porcelain", "--force-with-lease=" + ref + ":" + sha,
                       "origin", ":" + ref], env)
        if deleted.returncode:
            raise RuntimeError("Branch changed or deletion denied; not overriding: " + branch)
        print("Deleted fully merged branch: " + branch)

if __name__ == "__main__":
    main()
