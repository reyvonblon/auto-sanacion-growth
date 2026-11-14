#!/usr/bin/env python3
"""KDP SEO Optimizer & Validator for Amazon Books (Spanish/UTF-8 safe).

Validates Amazon KDP's 7 backend keyword boxes (strict 50-byte UTF-8 limit per box),
filters prohibited KDP terms, packs candidate keywords greedily into 7 boxes,
and validates KDP HTML book descriptions (<= 4000 characters, allowed tags only).
"""

from __future__ import annotations

import argparse
import json
import re
import unicodedata
from pathlib import Path
from typing import Iterable

MAX_KDP_BOX_BYTES = 50
MAX_KDP_BOXES = 7
MAX_DESCRIPTION_CHARS = 4000

ALLOWED_KDP_TAGS = {"b", "i", "br", "p", "ul", "ol", "li", "h4", "h5", "h6"}

PROHIBITED_TERMS = {
    "amazon",
    "kindle",
    "kdp",
    "gratis",
    "free",
    "bestseller",
    "best seller",
    "mas vendido",
    "nuevo",
    "new",
    "oferta",
    "descuento",
    "barato",
    "libro",
    "ebook",
}


def utf8_bytes(text: str) -> int:
    """Return exact UTF-8 byte length of a string."""
    return len(text.encode("utf-8"))


def normalize_token(text: str) -> str:
    """Lowercase and strip accents for duplicate/prohibited comparisons."""
    nfkd = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in nfkd if not unicodedata.combining(ch)).strip()


def find_prohibited_terms(text: str) -> list[str]:
    """Return any KDP-prohibited marketing terms found in text."""
    normalized = normalize_token(text)
    found: list[str] = []
    for term in sorted(PROHIBITED_TERMS):
        if re.search(rf"\b{re.escape(term)}\b", normalized):
            found.append(term)
    return found


def pack_keyword_boxes(
    phrases: Iterable[str],
    title_text: str = "",
    author_text: str = "",
    max_boxes: int = MAX_KDP_BOXES,
    max_bytes: int = MAX_KDP_BOX_BYTES,
) -> dict:
    """Pack candidate phrases into KDP backend boxes without exceeding 50 UTF-8 bytes.

    Amazon KDP indexes unique words across boxes, so punctuation/commas waste bytes
    and words already in title/author are redundant.
    """
    excluded_words = set()
    for source in (title_text, author_text):
        for w in re.findall(r"[\wáéíóúüñÁÉÍÓÚÜÑ]+", source):
            excluded_words.add(normalize_token(w))

    seen_words = set(excluded_words)
    boxes: list[str] = [""] * max_boxes
    skipped_prohibited: list[str] = []
    overflow_phrases: list[str] = []

    cleaned_candidates: list[str] = []
    for raw in phrases:
        phrase = " ".join(raw.replace(",", " ").split())
        if not phrase:
            continue
        prohibited = find_prohibited_terms(phrase)
        if prohibited:
            skipped_prohibited.append(f"{phrase} ({', '.join(prohibited)})")
            continue
        # Keep only words not already indexed in title/author/previous phrases
        kept_words: list[str] = []
        for word in phrase.split():
            norm = normalize_token(word)
            if norm and norm not in seen_words:
                seen_words.add(norm)
                kept_words.append(word)
        if kept_words:
            cleaned_candidates.append(" ".join(kept_words))

    box_idx = 0
    for chunk in cleaned_candidates:
        placed = False
        while box_idx < max_boxes:
            current = boxes[box_idx]
            candidate = f"{current} {chunk}".strip() if current else chunk
            if utf8_bytes(candidate) <= max_bytes:
                boxes[box_idx] = candidate
                placed = True
                break
            box_idx += 1
        if not placed:
            # Try fitting individual words if the whole chunk didn't fit in remaining space
            remaining_words = chunk.split()
            for word in remaining_words:
                word_placed = False
                for idx in range(max_boxes):
                    current = boxes[idx]
                    cand = f"{current} {word}".strip() if current else word
                    if utf8_bytes(cand) <= max_bytes:
                        boxes[idx] = cand
                        word_placed = True
                        break
                if not word_placed:
                    overflow_phrases.append(word)

    return {
        "boxes": [
            {
                "box_number": i + 1,
                "content": content,
                "utf8_bytes": utf8_bytes(content),
                "chars": len(content),
                "valid": utf8_bytes(content) <= max_bytes,
            }
            for i, content in enumerate(boxes)
        ],
        "skipped_prohibited": skipped_prohibited,
        "overflow_words": overflow_phrases,
    }


def validate_keyword_boxes(boxes: list[str]) -> dict:
    """Validate an existing list of up to 7 KDP keyword boxes."""
    results = []
    seen_words: dict[str, int] = {}
    duplicates: list[str] = []
    prohibited_hits: list[str] = []

    for idx, box in enumerate(boxes, start=1):
        b_len = utf8_bytes(box)
        prohibited = find_prohibited_terms(box)
        if prohibited:
            prohibited_hits.append(f"Box {idx}: {', '.join(prohibited)}")
        for word in re.findall(r"[\wáéíóúüñÁÉÍÓÚÜÑ]+", box):
            norm = normalize_token(word)
            if norm in seen_words:
                duplicates.append(f"'{word}' (Box {seen_words[norm]} & Box {idx})")
            else:
                seen_words[norm] = idx
        results.append(
            {
                "box_number": idx,
                "content": box,
                "utf8_bytes": b_len,
                "valid_bytes": b_len <= MAX_KDP_BOX_BYTES,
            }
        )

    return {
        "box_count_valid": len(boxes) <= MAX_KDP_BOXES,
        "boxes": results,
        "duplicate_words": duplicates,
        "prohibited_hits": prohibited_hits,
        "all_valid": (
            len(boxes) <= MAX_KDP_BOXES
            and all(r["valid_bytes"] for r in results)
            and not prohibited_hits
        ),
    }


def validate_kdp_description_html(html_text: str) -> dict:
    """Validate Amazon KDP HTML description tags and 4000-char limit."""
    tags = re.findall(r"</?([a-zA-Z0-9]+)(?:\s[^>]*)?/?>", html_text)
    unsupported = sorted({t.lower() for t in tags if t.lower() not in ALLOWED_KDP_TAGS})
    char_count = len(html_text)
    return {
        "char_count": char_count,
        "max_chars": MAX_DESCRIPTION_CHARS,
        "within_limit": char_count <= MAX_DESCRIPTION_CHARS,
        "unsupported_tags": unsupported,
        "valid": char_count <= MAX_DESCRIPTION_CHARS and not unsupported,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate or pack Amazon KDP SEO metadata.")
    parser.add_argument("--keywords-json", type=Path, help="JSON file with 'phrases' list, 'title', 'author'.")
    parser.add_argument("--description-html", type=Path, help="HTML file to validate for KDP description.")
    args = parser.parse_args()

    output: dict = {}
    if args.keywords_json:
        data = json.loads(args.keywords_json.read_text(encoding="utf-8"))
        if "boxes" in data:
            output["keyword_validation"] = validate_keyword_boxes(data["boxes"])
        elif "phrases" in data:
            output["keyword_packing"] = pack_keyword_boxes(
                phrases=data["phrases"],
                title_text=data.get("title", ""),
                author_text=data.get("author", ""),
            )

    if args.description_html:
        html_text = args.description_html.read_text(encoding="utf-8")
        output["description_validation"] = validate_kdp_description_html(html_text)

    print(json.dumps(output, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
