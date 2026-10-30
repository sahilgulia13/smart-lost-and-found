
import unittest

from linked_list import LinkedList
from matching import calculate_match_score, find_possible_matches
from generate_dataset import generate_records


class TestLinkedList(unittest.TestCase):

    def setUp(self):
        self.items = LinkedList()

    def test_append_and_length(self):
        self.items.append({"item_id": "LF0001"})
        self.items.append({"item_id": "LF0002"})
        self.assertEqual(len(self.items), 2)

    def test_find_existing_item(self):
        item = {"item_id": "LF0001", "item_name": "Wallet"}
        self.items.append(item)
        self.assertEqual(self.items.find_by_id("LF0001"), item)

    def test_find_missing_item(self):
        self.assertIsNone(self.items.find_by_id("UNKNOWN"))

    def test_delete_item(self):
        self.items.append({"item_id": "LF0001"})
        self.assertTrue(self.items.delete_by_id("LF0001"))
        self.assertEqual(len(self.items), 0)

    def test_delete_missing_item(self):
        self.assertFalse(self.items.delete_by_id("UNKNOWN"))


class TestMatching(unittest.TestCase):

    def setUp(self):
        self.lost = {
            "item_id": "L001",
            "report_type": "Lost",
            "item_name": "Black Wallet",
            "category": "Accessories",
            "brand": "Puma",
            "color": "Black",
            "location": "Library",
            "description": "Black leather wallet",
            "status": "Active"
        }

        self.found = {
            "item_id": "F001",
            "report_type": "Found",
            "item_name": "Black Wallet",
            "category": "Accessories",
            "brand": "Puma",
            "color": "Black",
            "location": "Library",
            "description": "Black leather wallet",
            "status": "Active"
        }

    def test_identical_items_score_100(self):
        score = calculate_match_score(self.lost, self.found)
        self.assertEqual(score, 100.0)

    def test_different_categories_score_zero(self):
        different = dict(self.found, category="Electronics")
        self.assertEqual(
            calculate_match_score(self.lost, different), 0
        )

    def test_matching_returns_candidate(self):
        matches = find_possible_matches(self.lost, [self.found])
        self.assertEqual(len(matches), 1)
        self.assertEqual(matches[0]["item_id"], "F001")

    def test_inactive_item_is_excluded(self):
        inactive = dict(self.found, status="Returned")
        matches = find_possible_matches(self.lost, [inactive])
        self.assertEqual(matches, [])

    def test_matches_are_sorted_by_score(self):
        weaker = dict(
            self.found,
            item_id="F002",
            item_name="Wallet",
            location="Sports Ground",
            description="Small wallet",
            brand="Unknown"
        )

        matches = find_possible_matches(
            self.lost, [weaker, self.found]
        )

        scores = [match["score"] for match in matches]
        self.assertEqual(scores, sorted(scores, reverse=True))


class TestDataset(unittest.TestCase):

    def test_generates_1000_records(self):
        records = generate_records(1000)
        self.assertEqual(len(records), 1000)

    def test_dataset_ids_are_unique(self):
        records = generate_records(1000)
        ids = [record["item_id"] for record in records]
        self.assertEqual(len(ids), len(set(ids)))

    def test_expected_fields_exist(self):
        record = generate_records(1)[0]
        expected = {
            "item_id", "report_type", "item_name", "category",
            "brand", "color", "location", "description",
            "date_reported", "contact", "status"
        }
        self.assertEqual(set(record.keys()), expected)


if __name__ == "__main__":
    unittest.main(verbosity=2)
