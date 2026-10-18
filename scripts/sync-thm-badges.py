#!/usr/bin/env python3
"""Refresh public TryHackMe earned badge records for the AYUSH.SEC static site.

Uses an observed, unofficial public endpoint. No account cookies/passwords are used.
The endpoint/schema can change; failed fetches do not overwrite the last good JSON.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urljoin, urlparse

BASE = "https://tryhackme.com"
PROFILE_URL = "https://tryhackme.com/p/Kshatantra"
NAME_KEYS = ("name", "badgeName", "badge_name", "title", "displayName", "display_name", "achievementName", "label")
IMAGE_KEYS = ("image", "imageUrl", "imageURL", "image_url", "img", "imgUrl", "icon", "iconUrl", "iconURL", "icon_url", "badgeImage", "badgeImageUrl", "badge_image", "badge_image_url", "imagePath", "iconPath", "thumbnail", "artwork")
DATE_KEYS = ("earnedAt", "earned_at", "awardedAt", "awarded_at", "dateEarned", "date_earned", "createdAt", "created_at", "date")


class SyncError(RuntimeError):
    pass


def scalar_text(value: Any) -> str | None:
    if isinstance(value, str) and value.strip():
        return value.strip()[:180]
    return None


def normalize_url(value: Any) -> str | None:
    if not isinstance(value, str) or not value.strip():
        return None
    value = value.strip()
    if value.startswith("//"):
        value = "https:" + value
    elif value.startswith("/"):
        value = urljoin(BASE, value)
    parsed = urlparse(value)
    if parsed.scheme != "https" or not parsed.netloc:
        return None
    return value


def first_scalar(obj: dict[str, Any], keys: tuple[str, ...]) -> str | None:
    for key in keys:
        if key in obj:
            val = scalar_text(obj[key])
            if val:
                return val
    return None


def find_image(obj: dict[str, Any]) -> str | None:
    for key in IMAGE_KEYS:
        value = obj.get(key)
        if isinstance(value, str):
            found = normalize_url(value)
            if found:
                return found
        elif isinstance(value, dict):
            for nested_key in ("url", "src", "href", "path", "original", "large", "medium"):
                found = normalize_url(value.get(nested_key))
                if found:
                    return found
    # Some responses name an image field generically as `url`; only accept clear image paths.
    for key in ("url", "src", "href"):
        value = obj.get(key)
        if isinstance(value, str) and re.search(r"\.(?:png|jpe?g|gif|webp|svg)(?:[?#].*)?$", value, re.I):
            found = normalize_url(value)
            if found:
                return found
    return None


def find_date(obj: dict[str, Any]) -> str | None:
    for key in DATE_KEYS:
        val = obj.get(key)
        if isinstance(val, str) and val.strip():
            return val.strip()[:40]
    return None


def collect_badges(payload: Any) -> list[dict[str, str]]:
    found: list[dict[str, str]] = []
    visited: set[int] = set()

    def walk(node: Any, depth: int = 0) -> None:
        if depth > 12:
            return
        if isinstance(node, dict):
            ident = id(node)
            if ident in visited:
                return
            visited.add(ident)
            # Try both the current object and common nested badge descriptors.
            candidate = dict(node)
            for nested_key in ("badge", "achievement", "item", "award", "badgeInfo", "badge_info"):
                nested = node.get(nested_key)
                if isinstance(nested, dict):
                    merged = dict(node)
                    merged.update(nested)
                    candidate = merged
                    name = first_scalar(candidate, NAME_KEYS)
                    image = find_image(candidate)
                    if name and image:
                        found.append({"name": name, "image": image, "earned_at": find_date(node) or ""})
            name = first_scalar(candidate, NAME_KEYS)
            image = find_image(candidate)
            if name and image:
                found.append({"name": name, "image": image, "earned_at": find_date(node) or ""})
            for val in node.values():
                if isinstance(val, (dict, list)):
                    walk(val, depth + 1)
        elif isinstance(node, list):
            for item in node:
                walk(item, depth + 1)

    walk(payload)
    deduped: list[dict[str, str]] = []
    seen = set()
    for badge in found:
        key = (badge["name"].casefold(), badge["image"])
        if key in seen:
            continue
        seen.add(key)
        badge["profile_url"] = PROFILE_URL
        deduped.append(badge)
    return deduped


def fetch_payload(username: str) -> Any:
    try:
        from curl_cffi import requests as c_requests
    except ImportError as exc:
        raise SyncError("Missing curl_cffi. Activate the setup virtual environment and install it with: pip install curl_cffi") from exc

    endpoint = f"{BASE}/api/v2/users/badges"
    try:
        response = c_requests.get(
            endpoint,
            params={"username": username},
            impersonate="chrome",
            timeout=25,
            headers={
                "Accept": "application/json",
                "Referer": f"{BASE}/p/{username}",
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36",
            },
        )
    except Exception as exc:
        raise SyncError(f"Could not reach TryHackMe. Check internet or endpoint availability. Details: {exc}") from exc

    if response.status_code in (403, 429, 503):
        raise SyncError(f"TryHackMe returned HTTP {response.status_code} (possibly a temporary checkpoint/rate limit). No files were overwritten; wait and try later once, rather than retrying rapidly.")
    if response.status_code != 200:
        raise SyncError(f"TryHackMe badge endpoint returned HTTP {response.status_code}. It may have changed; no files were overwritten.")
    content_type = response.headers.get("content-type", "").lower()
    body = response.text
    if "json" not in content_type and not body.lstrip().startswith(("{", "[")):
        raise SyncError("TryHackMe returned a non-JSON page (possibly an anti-bot check). No files were overwritten.")
    try:
        return response.json()
    except Exception as exc:
        raise SyncError("TryHackMe response was not valid JSON. No files were overwritten.") from exc


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", default="Kshatantra")
    parser.add_argument("--output", default="assets/thm_badges.json")
    args = parser.parse_args()
    output = Path(args.output)
    if not output.is_absolute():
        output = Path.cwd() / output

    try:
        payload = fetch_payload(args.username)
    except SyncError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    badges = collect_badges(payload)
    if not badges:
        print("ERROR: The endpoint returned no recognizable badge records with image URLs. Its schema may have changed; existing gallery data was kept unchanged.", file=sys.stderr)
        print("Tip: run once manually and inspect only the public JSON shape locally; do not share cookies or account data.", file=sys.stderr)
        return 3

    doc = {
        "username": args.username,
        "updated_at": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
        "source": "TryHackMe public badges endpoint (observed/unofficial; schema may change)",
        "status": "synced",
        "count": len(badges),
        "badges": badges,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    tmp = output.with_suffix(output.suffix + ".tmp")
    tmp.write_text(json.dumps(doc, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(output)
    print(f"Updated {output} with {len(badges)} real badge image records for {args.username}.")
    print("Next: review the JSON, then commit/push it with your normal website sync script.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
