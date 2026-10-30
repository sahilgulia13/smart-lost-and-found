# Smart Lost & Found Management System

## Project Overview

The Smart Lost & Found Management System is a Python-based desktop application designed to manage lost and found items on a college campus. It allows users to report items, search records, filter reports, update item status, and identify possible matches between lost and found reports.

The project demonstrates Data Structures and Algorithms (DSA) through a linked list, text similarity calculation, searching, and sorting.

## Team Details

- **Sahil** — 251302023
- **University:** SGT University
- **School:** School of Engineering and Technology (SOET)
- **Department:** Computer Science and Engineering (AI & ML)

## Technologies Used

- Python 3
- Tkinter and ttk for the graphical user interface
- CSV for data storage
- Linked list for record management
- `difflib.SequenceMatcher` for text similarity
- Python `unittest` for automated testing

## Features

1. View lost and found records.
2. Search records using item details.
3. Filter records by report type and status.
4. Submit new lost or found reports.
5. Calculate similarity scores to suggest possible matches.
6. Sort match suggestions by score.
7. Update records to Active, Claimed, or Returned.
8. Store records in a CSV file.
9. Generate 1,000 synthetic sample records.
10. Run automated tests.

## Project Structure

```text
Smart_Lost_and_Found/
├── main.py
├── linked_list.py
├── matching.py
├── generate_dataset.py
├── lost_found_dataset.csv
├── tests.py
└── README.md
```

## Requirements

- Python 3
- A working Tkinter installation
- VS Code or another Python editor

No third-party Python packages are required for the current implementation.

## How to Run

1. Open the project folder in VS Code.
2. Open the terminal in that folder.
3. If the dataset is missing, generate it:

   `python3 generate_dataset.py`

4. Launch the application:

   `python3 main.py`

The application generates the initial dataset automatically if the CSV file is absent.

## How to Run Automated Tests

Run:

`python3 -m unittest tests.py -v`

The tests cover linked-list operations, match scoring, match ordering, inactive-record exclusion, and dataset generation.

## Data Structures and Algorithms

### Linked List

Each node stores an item record and a reference to the next node. The linked list supports insertion, traversal, ID-based searching, and deletion.

### Text Similarity

`SequenceMatcher` compares the text of two fields and produces a similarity ratio.

### Matching Algorithm

The matching score uses the following weights:

- Item name: 35%
- Location: 25%
- Description: 25%
- Brand: 15%

Items in different categories receive a score of zero. Candidate matches are sorted in descending score order. The default minimum score for suggestions is 35.

### Complexity

Let \(n\) be the number of stored records and \(m\) the number of found-item candidates.

- Linked-list traversal: \(O(n)\)
- ID-based search: \(O(n)\)
- Appending to the linked list: \(O(n)\) in the current implementation
- Matching candidates: \(O(m)\) score calculations, plus sorting in \(O(k\log k)\), where \(k\) is the number of qualifying matches

Text-comparison costs depend on the lengths of the compared strings.

## Dataset

The dataset generator creates synthetic sample records with fields such as:

- Item ID
- Report type
- Item name
- Category
- Brand
- Colour
- Location
- Description
- Report date
- Contact placeholder
- Status

The records are for demonstration and testing, not real campus reports.

## Limitations

- The application uses local CSV storage rather than a central database.
- Match scores are heuristic suggestions and do not establish ownership.
- There is no login system or role-based access control.
- The application does not send notifications.

## Future Scope

- Integrate SQLite or another database.
- Add user authentication and administrator access.
- Improve match ranking with additional attributes.
- Add image uploads and notifications.
- Add secure claim verification and audit logs.

## Conclusion

The project demonstrates how Python, GUI development, data storage, linked lists, searching, sorting, and text similarity can be combined to create a functional campus lost-and-found management application.

**Note:** All sample records are synthetic. Ownership should be verified before an item is returned.
