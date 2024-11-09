from node import Node

class AVLTree:
    def __init__(self, compare_function):
        self.root = None
        self.size = 0
        self.comparator = compare_function  # Comparator function to determine node ordering

    def get_height(self, node):
        if node is None:
            return 0
        return node.height

    def balance_factor(self, node):
        if node is None:
            return 0
        return self.get_height(node.right) - self.get_height(node.left)

    def update_height(self, node):
        node.height = 1 + max(self.get_height(node.left), self.get_height(node.right))

    def right_rotation(self, y):
        # Ensure that the left child is not None
        if y.left is None:
            return y  # No rotation can be performed

        x = y.left
        T2 = x.right

        # Perform rotation
        x.right = y
        y.left = T2

        # Update heights
        self.update_height(y)
        self.update_height(x)

        return x


    def left_rotation(self, x):
        if x.right is None:
            return x  # No rotation can be performed

        y = x.right
        T2 = y.left

        # Perform rotation
        y.left = x
        x.right = T2

        # Update heights
        self.update_height(x)
        self.update_height(y)

        return y

    def balance(self, root, val):
        bf = self.balance_factor(root)
        # Left-left case
        if bf < -1 and root.left is not None and self.comparator(val, root.left.key) < 0:
            root = self.right_rotation(root)
        # Right-right case
        if bf > 1 and root.right is not None and self.comparator(val, root.right.key) > 0:
            root = self.left_rotation(root)
        # Left-right case
        if bf < -1 and root.left is not None and  self.comparator(val, root.left.key) > 0:
            root.left = self.left_rotation(root.left)
            root = self.right_rotation(root)
        # Right-left case
        if bf > 1 and  root.right is not None and self.comparator(val, root.right.key) < 0:
            root.right = self.right_rotation(root.right)
            root = self.left_rotation(root)
        self.update_height(root)
        return root

    def insert(self, val):
        def insert_util(root, val):
            if root is None:
                return Node(val)
            if self.comparator(val, root.key) < 0:
                root.left = insert_util(root.left, val)
            elif self.comparator(val, root.key ) > 0:
                root.right = insert_util(root.right, val)
            
            self.update_height(root)
            root = self.balance(root, val)
            return root

        self.root = insert_util(self.root, val)

    def delete(self, data):
        def delete_util(root, data):
            if root is None:
                return None
            if self.comparator(data, root.key) > 0:
                root.right = delete_util(root.right, data)
            elif self.comparator(data, root.key) < 0:
                root.left = delete_util(root.left, data)
            else:
                if root is not None and root.left is None:
                    return root.right
                if root is not None and root.right is None:
                    return root.left
                temp = self.get_min_value_node(root.right)
                root.key = temp.key
                root.right = delete_util(root.right, temp.key)
            
            root = self.balance(root, data)
            return root

        self.root = delete_util(self.root, data)

    def get_min_value_node(self, root):
        while root.left is not None:
            root = root.left
        return root

    def print_tree(self):
        def inorder_util(root):
            if root is None:
                return
            inorder_util(root.left)
            print(f"Bin ID: {root.key.bin_id}, Remaining Capacity: {root.key.remaining_capacity}")
            inorder_util(root.right)

        if self.root is not None:
            inorder_util(self.root)
        else:
            print("Tree is empty")
    
    def print_obj_tree(self):
        def inorder_util(root):
            if root is None:
                return
            inorder_util(root.left)
            print(f"Object ID: {root.key.obj_id}, Size: {root.key.size}, Color: {root.key.color}")
            inorder_util(root.right)

        if self.root is not None:
            inorder_util(self.root)
        else:
            print("Object Tree is empty")

