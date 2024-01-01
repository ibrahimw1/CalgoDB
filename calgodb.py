# Import necessary libraries
import sys
import json
import hashlib
import argparse

# Start HashTable

class HashTable:
    def __init__(self, size=1000):
        # Initialize the hash table with a specified size
        self.size = size
        self.arr = [None] * self.size

    def sha1_hash(self, key):
        # Hash function using SHA1 algorithm
        sha1 = hashlib.sha1()
        sha1.update(str(key).encode())
        return int(sha1.hexdigest(), 16)

    def hash(self, key):
        # Hash the key using SHA1 and map it to the table size
        return self.sha1_hash(key) % self.size

    def find(self, key, value):
        # Find a value in the hash table given a key
        index = self.hash(key)
        if self.arr[index]:
            # If there's a collision, delegate to AVL tree's find method
            node = self.arr[index].find(key, value)
            if node:
                return node.value  # Return the actual data or value from the AVL node.
        return None

    def insert(self, key, value, title, content):
        # Insert a new value into the hash table
        index = self.hash(key)
        if not self.arr[index]:
            # If the slot is empty, create a new AVL tree
            self.arr[index] = AVLTree()
        # Insert the value into the AVL tree
        self.arr[index].insert(key, value, title, content)

    def delete(self, key):
        # Delete a value from the hash table
        index = self.hash(key)
        if self.arr[index]:
            # Delegate to AVL tree's delete method
            self.arr[index].delete(key)
    
    def get(self, primary_key, sort_key): # rename find to get
        # Get a value from the hash table using primary and sort keys
        index = self.hash(primary_key)
        if self.arr[index]:
            # Delegate to AVL tree's find method
            return self.arr[index].find(primary_key, sort_key)  # This calls AVL's 'get' method
        return None

# End HashTable

# Start AVL

class AVLNode:
    def __init__(self, key, value, title, content):
        # Initialize AVL tree node with key, value, title, and content
        self.key = key  # Tuple (primary_key, sort_key)
        self.value = value  # Actual data
        self.title = title
        self.content = content
        self.left = None
        self.right = None
        self.height = 1

class AVLTree:
    def __init__(self):
        # Initialize AVL tree
        self.root = None

    # Helper methods for AVL
    def height(self, node):
        # Get the height of a node
        if node is None:
            return 0
        return node.height

    def update_height(self, node):
        # Update the height of a node based on its children's heights
        node.height = max(self.height(node.left), self.height(node.right)) + 1

    def balance_factor(self, node):
        # Get the balance factor of a node (difference in heights between right and left children)
        if node is None:
            return 0
        return self.height(node.right) - self.height(node.left)

    def rotate_right(self, z):
        # Right rotation to balance the tree
        y = z.left
        z.left = y.right
        y.right = z
        self.update_height(z)
        self.update_height(y)
        return y

    def rotate_left(self, y):
        # Left rotation to balance the tree
        x = y.right
        y.right = x.left
        x.left = y
        self.update_height(y)
        self.update_height(x)
        return x

    def rebalance(self, node):
        # Rebalance the AVL tree
        self.update_height(node)
        balance = self.balance_factor(node)
        if balance < -1:
            if self.balance_factor(node.left) > 0:
                node.left = self.rotate_left(node.left)
            return self.rotate_right(node)
        if balance > 1:
            if self.balance_factor(node.right) < 0:
                node.right = self.rotate_right(node.right)
            return self.rotate_left(node)
        return node

    def insert(self, key, value, title, content):
        # Insert a new node into the AVL tree
        self.root = self._insert(self.root, key, value, title, content)

    def _insert(self, node, key, value, title, content):
        # Recursive helper function for insertion
        # Sort duplicates by updating existing node
        if node is None:
            return AVLNode(key, value, title, content)
        
        if key == node.key:
            node.value = value
            node.title = title
            node.content = content
            return node

        if key < node.key:
            node.left = self._insert(node.left, key, value, title, content)
        else:
            node.right = self._insert(node.right, key, value, title, content)
        return self.rebalance(node)

    def delete(self, key):
        # Delete a node from the AVL tree
        self.root = self._delete(self.root, key)

    def _delete(self, node, key):
        # Recursive helper function for deletion
        if node is None:
            return node
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Replace the node with its in-order successor
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            temp = self._find_min(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete(node.right, temp.key)
        return self.rebalance(node)

    def _find_min(self, node):
        # Find the node with the minimum key value in the tree
        current = node
        while current.left:
            current = current.left
        return current

    def find(self, key, value):
        # Find a node in the AVL tree based on key
        return self._find(self.root, key, value)

    def _find(self, node, key, value):
        # Recursive helper function for finding a node
        if node is None:
            return None
        if key == node.key:
            return node
        elif key < node.key:
            return self._find(node.left, key)
        else:
            return self._find(node.right, key)
    
    def get(self, primary_key, sort_key):
        # Get a value from the AVL tree using primary and sort keys
        key = (primary_key, sort_key)
        node = self._find(self.root, key)
        if node:
            return node.value
        return None
    
    def traversal_order(self):
        # Get the nodes of the AVL tree in-order traversal
        result = []
        self._traversal_order(self.root, result)
        return result

    def _traversal_order(self, node, result):
        # Recursive helper function for in-order traversal
        if node is not None:
            self._traversal_order(node.left, result)
            result.append(node)  # return the entire node instead of just the key
            self._traversal_order(node.right, result)

# End AVL

class CalgoDB:
    def __init__(self, capacity=1000):
        # Initialize CalgoDB with a specified capacity
        self.table = HashTable(capacity)

    def put_item(self, data_file):
        # Add or update records in the database from a JSON file
        with open(data_file, 'r') as f:
            data_list = json.load(f)
            for data in data_list:
                primary_key = data.get("note_holder", "")
                sort_key = data.get("note_created_date", 0)
                title = data.get("note_title", "")
                content = data.get("note_content", "")
                self.table.insert(primary_key, sort_key, title, content)

    def get_item(self, key_file):
        # Retrieve a record from the database based on keys provided in a JSON file
        with open(key_file, 'r') as f: 
            key_data = json.load(f)
            primary_key = key_data.get("note_holder", "")
            sort_key = key_data.get("note_created_date", 0)
            result = self.table.get(primary_key, sort_key)
            if result is not None:
                title, content = result.title, result.content
                print("Retrieved:", primary_key, sort_key, title, content)
            else:
                print("Item not found:", primary_key, sort_key)
                
    def query(self, primary_key):
        # Return all records with a given primary key, sorted by the sort key
        avl_tree = self.table.arr[self.table.hash(primary_key)]
        
        if not avl_tree or not avl_tree.root:
            print(f"No records found for primary key: {primary_key}")
            return
        
        nodes = avl_tree.traversal_order()
        
        print("| note_holder           | note_created_date | note_title  | note_content                                |")
        print("|-----------------------|-------------------|-------------|---------------------------------------------|")
        for node in nodes:
            print(f"| {primary_key:23} | {node.value:17} | {node.title:11} | {node.content:45} |")

if __name__ == "__main__":
    db = CalgoDB()

    if len(sys.argv) < 3:
        print("Insufficient arguments provided.")
        sys.exit(1)

    command = sys.argv[1]
    filename = sys.argv[2]

    if command == "put_item":
        db.put_item(filename)
        print("Success")
    elif command == "get_item":
        db.put_item('input_data.json')
        db.get_item(filename)
    elif command == "query":
        db.put_item('input_data.json')
        db.query(sys.argv[2])
    else:
        print(f"Unknown command: {command}")
