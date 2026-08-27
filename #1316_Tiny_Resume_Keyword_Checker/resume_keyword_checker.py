#!/usr/bin/env python3
"""
Tiny Resume Keyword Checker
Compare resume text with a job description and score keyword matches.

Usage:
    python resume_keyword_checker.py resume.txt job_description.txt
"""

import re
import sys
from collections import Counter
from typing import List, Tuple


# Common English stop words that carry little signal in a job description
STOP_WORDS = {
    "a", "an", "the", "and", "or", "but", "if", "of", "in", "on", "at",
    "to", "for", "with", "by", "as", "is", "are", "was", "were", "be",
    "been", "being", "have", "has", "had", "do", "does", "did", "will",
    "would", "can", "could", "should", "may", "might", "must", "not",
    "no", "yes", "so", "than", "then", "that", "this", "these", "those",
    "it", "its", "we", "you", "they", "he", "she", "from", "about",
    "into", "over", "after", "before", "between", "under", "up", "down",
    "out", "off", "just", "all", "any", "each", "some", "such", "only",
    "also", "very", "more", "most", "other", "own", "both", "same",
}


def tokenize(text: str) -> List[str]:
    """Split text into lowercase word tokens."""
    return re.findall(r"[a-z0-9][a-z0-9+\-\.]*", text.lower())


def extract_keywords(job_text: str) -> List[str]:
    """Extract meaningful keywords from a job description.

    Returns words that appear at least twice in the description (so the
    most emphasized skills surface), excluding stop words and single
    characters.
    """
    tokens = [t for t in tokenize(job_text) if t not in STOP_WORDS and len(t) > 1]
    counts = Counter(tokens)
    # Keywords the posting repeats, plus anything that looks like a skill term
    repeated = {w for w, c in counts.items() if c >= 2}
    # Include single-mention words that are longer (e.g. "kubernetes")
    long = {w for w, c in counts.items() if c == 1 and len(w) >= 6}
    return sorted(repeated | long)


def score_resume(resume_text: str, keywords: List[str]) -> Tuple[List[str], List[str], float]:
    """Match resume text against keywords.

    Returns (matched, missing, score) where score is the fraction of
    keywords found in the resume (0.0 - 1.0).
    """
    resume_words = set(tokenize(resume_text))
    matched = [k for k in keywords if k in resume_words]
    missing = [k for k in keywords if k not in resume_words]
    if not keywords:
        return [], [], 0.0
    return matched, missing, len(matched) / len(keywords)


def main(argv: List[str]) -> int:
    if len(argv) != 3:
        print(__doc__)
        return 2

    resume_path, job_path = argv[1], argv[2]
    try:
        resume_text = open(resume_path, encoding="utf-8").read()
        job_text = open(job_path, encoding="utf-8").read()
    except OSError as e:
        print(f"Error reading input files: {e}", file=sys.stderr)
        return 1

    keywords = extract_keywords(job_text)
    matched, missing, score = score_resume(resume_text, keywords)

    print(f"Keywords extracted from job description: {len(keywords)}")
    print(f"Matched in resume: {len(matched)}/{len(keywords)}")
    print(f"Score: {score:.0%}")
    print()
    if matched:
        print("Matched:")
        for k in matched:
            print(f"  + {k}")
    if missing:
        print("Missing:")
        for k in missing:
            print(f"  - {k}")

    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
