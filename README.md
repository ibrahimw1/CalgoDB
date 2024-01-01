# CalgoDB

CalgoDB is a simple document database implemented in Python, featuring a hash table with dynamic arrays and an AVL tree for efficient key-based operations. The database supports composite keys, consisting of a primary key and a sort key.

## Features

- **Hash Table:** Utilizes a hash table with a dynamic array, implementing the SHA1 algorithm for hashing.
- **Collision Handling:** Uses an AVL tree to handle collisions, ensuring worst-case O(logn) search time.
- **Put Item:** Adds or updates records in the database from a JSON file.
- **Get Item:** Retrieves a record from the database based on keys provided in a JSON file.
- **Query:** Returns all records with a given primary key, sorted by the sort key, in O(logn) time.
