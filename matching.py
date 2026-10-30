
from difflib import SequenceMatcher


def similarity(text1, text2):
    """Calculate text similarity between 0 and 1."""
    text1 = str(text1).strip().lower()
    text2 = str(text2).strip().lower()

    if not text1 or not text2:
        return 0.0

    return SequenceMatcher(None, text1, text2).ratio()


def calculate_match_score(lost_item, found_item):
    """
    Compare a lost-item report with a found-item report.
    Returns a score from 0 to 100.
    """

    # Different categories cannot be matched.
    if lost_item.get("category", "").lower() != found_item.get(
        "category", ""
    ).lower():
        return 0

    score = 0.0

    # Item names: maximum 35 points.
    name_score = similarity(
        lost_item.get("item_name", ""),
        found_item.get("item_name", "")
    )
    score += name_score * 35

    # Locations: maximum 25 points.
    location_score = similarity(
        lost_item.get("location", ""),
        found_item.get("location", "")
    )
    score += location_score * 25

    # Descriptions: maximum 25 points.
    description_score = similarity(
        lost_item.get("description", ""),
        found_item.get("description", "")
    )
    score += description_score * 25

    # Brand: maximum 15 points.
    brand_score = similarity(
        lost_item.get("brand", ""),
        found_item.get("brand", "")
    )
    score += brand_score * 15

    return round(score, 2)


def find_possible_matches(lost_item, found_items, minimum_score=35):
    """Return found items with sufficiently high match scores."""

    matches = []

    for found_item in found_items:
        if found_item.get("status", "Active").lower() != "active":
            continue

        score = calculate_match_score(lost_item, found_item)

        if score >= minimum_score:
            matches.append({
                "item_id": found_item.get("item_id", ""),
                "item_name": found_item.get("item_name", ""),
                "category": found_item.get("category", ""),
                "location": found_item.get("location", ""),
                "score": score,
                "found_item": found_item
            })

    # Highest-scoring possible matches appear first.
    matches.sort(key=lambda match: match["score"], reverse=True)

    return matches
