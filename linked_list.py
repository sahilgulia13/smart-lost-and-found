
class Node:
    """A single node in the linked list."""

    def __init__(self, item):
        self.item = item
        self.next = None


class LinkedList:
    """Linked list used to store lost and found item records."""

    def __init__(self):
        self.head = None
        self.size = 0

    def append(self, item):
        """Add an item record to the end of the list."""
        new_node = Node(item)

        if self.head is None:
            self.head = new_node
        else:
            current = self.head

            while current.next is not None:
                current = current.next

            current.next = new_node

        self.size += 1

    def get_all(self):
        """Return all records as a Python list."""
        records = []
        current = self.head

        while current is not None:
            records.append(current.item)
            current = current.next

        return records

    def find_by_id(self, item_id):
        """Find an item using its unique ID."""
        current = self.head

        while current is not None:
            if current.item.get("item_id") == item_id:
                return current.item

            current = current.next

        return None

    def delete_by_id(self, item_id):
        """Delete a record using its unique ID."""
        current = self.head
        previous = None

        while current is not None:
            if current.item.get("item_id") == item_id:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next

                self.size -= 1
                return True

            previous = current
            current = current.next

        return False

    def __len__(self):
        return self.size

    def is_empty(self):
        return self.size == 0
