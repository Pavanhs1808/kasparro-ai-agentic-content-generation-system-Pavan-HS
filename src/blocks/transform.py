from typing import List, Dict, Optional


PUNCTUATION_MAP = {
    "\u2013": "-",  # en dash
    "\u2014": "-",  # em dash
}


def normalize_punctuation(text: Optional[str]) -> Optional[str]:
    if text is None:
        return None
    out = text
    for src, dst in PUNCTUATION_MAP.items():
        out = out.replace(src, dst)
    return out


def join_list(items: List[str]) -> str:
    return ", ".join(items) if items else "Not specified"


def fmt_price(price: Optional[str]) -> str:
    # Keep as provided but ensure punctuation normalized
    if not price:
        return "Not specified"
    return normalize_punctuation(price) or "Not specified"


def normalize_skin_types(types: List[str]) -> List[str]:
    return [t.strip().capitalize() for t in types]


def bullet_list(items: List[str]) -> str:
    if not items:
        return "Not specified"
    return "\n".join(f"- {i}" for i in items)


def compare_lists(a: List[str], b: List[str]) -> Dict[str, List[str]]:
    sa, sb = set(map(str.lower, a)), set(map(str.lower, b))
    overlap = sorted(sa & sb)
    only_a = sorted(sa - sb)
    only_b = sorted(sb - sa)
    return {
        "overlap": [s.title() for s in overlap],
        "only_a": [s.title() for s in only_a],
        "only_b": [s.title() for s in only_b],
    }


def summarize_comparison(section: str, overlap: List[str], only_a: List[str], only_b: List[str]) -> str:
    if not overlap and not only_a and not only_b:
        return f"No {section.lower()} data available for comparison."
    parts = []
    if overlap:
        parts.append(f"Shared {section.lower()}: {', '.join(overlap)}")
    if only_a:
        parts.append(f"Unique to A: {', '.join(only_a)}")
    if only_b:
        parts.append(f"Unique to B: {', '.join(only_b)}")
    return "; ".join(parts)
