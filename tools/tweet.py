#!/usr/bin/env python3
"""Post a tweet for a published blog post."""

import sys
import os
from pathlib import Path
import hashlib

def load_env():
    env_path = Path(__file__).resolve().parent.parent / ".env"
    if not env_path.exists():
        print(f"ERROR: .env not found at {env_path}", file=sys.stderr)
        sys.exit(1)
    env = {}
    for line in env_path.read_text().strip().splitlines():
        if "=" in line and not line.startswith("#"):
            k, v = line.split("=", 1)
            env[k.strip()] = v.strip()
    return env

def extract_post_info(md_path: str) -> dict:
    text = Path(md_path).read_text(encoding="utf-8")
    lines = text.split("\n")
    in_frontmatter = False
    title = Path(md_path).stem
    tags = []
    description = ""

    for line in lines:
        stripped = line.strip()
        if stripped == "---":
            if not in_frontmatter:
                in_frontmatter = True
                continue
            else:
                break
        if in_frontmatter:
            if stripped.startswith("description:"):
                description = stripped.split(":", 1)[1].strip().strip('"').strip("'")
            if stripped.startswith("- ") and tags is not None:
                tag = stripped[2:].strip().strip('"').strip("'")
                tags.append(tag)
            if stripped.startswith("tags:"):
                tags = []

    return {"title": title, "tags": tags, "description": description}

def build_tweet(info: dict, url: str) -> str:
    parts = [info["title"]]
    if info["description"]:
        parts.append(info["description"])
    parts.append("")
    hashtags = " ".join(f"#{t}" for t in info["tags"] if t not in ("Headliner",))
    if hashtags:
        parts.append(hashtags)
    parts.append(url)
    tweet = "\n".join(parts)
    if len(tweet) > 280:
        tweet = f"{info['title']}\n\n{hashtags}\n{url}" if hashtags else f"{info['title']}\n\n{url}"
    if len(tweet) > 280:
        tweet = f"{info['title']}\n{url}"
    return tweet

def post_tweet(tweet_text: str, env: dict):
    import tweepy
    auth = tweepy.OAuth1UserHandler(
        env["X_API_KEY"], env["X_API_SECRET"],
        env["X_ACCESS_TOKEN"], env["X_ACCESS_TOKEN_SECRET"],
    )
    api = tweepy.API(auth)
    status = api.update_status(tweet_text)
    print(f"OK tweet_id={status.id}")
    return status.id

def main():
    if len(sys.argv) < 2:
        print("Usage: tweet.py <markdown_file> [blog_url]", file=sys.stderr)
        sys.exit(1)

    md_path = sys.argv[1]
    info = extract_post_info(md_path)

    slug = Path(md_path).stem
    base_url = "https://startedourmission.github.io"
    hash_id = hashlib.md5(slug.encode("utf-8")).hexdigest()[:8]
    blog_url = sys.argv[2] if len(sys.argv) > 2 else f"{base_url}/{hash_id}.html"

    env = load_env()
    tweet_text = build_tweet(info, blog_url)

    print(f"--- Tweet preview ---\n{tweet_text}\n--- ({len(tweet_text)} chars) ---")

    if os.environ.get("DRY_RUN") == "1":
        print("DRY_RUN=1, skipping post")
        return

    post_tweet(tweet_text, env)

if __name__ == "__main__":
    main()
