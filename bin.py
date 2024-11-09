from avl import AVLTree
class Bin:
    def __init__(self, bin_id, capacity):
        def comp(node1, node2):
            if node1.obj_id < node2.obj_id:
                return -1
            elif node1.obj_id > node2.obj_id:
                return 1
            else:
                return 0
        
        self.bin_id = bin_id
        # self.Max_capacity = capacity
        self.remaining_capacity = capacity
        self.obj_tree = AVLTree(comp)
        self.height = 1

    def add_object(self, object):
        self.obj_tree.insert(object)
        self.remaining_capacity -= object.size

    def remove_object(self, object):
        self.obj_tree.delete(object)

    def objects_list(self):
        def inorder_traversal(node, result):
            if node:
                inorder_traversal(node.left, result)
                result.append(node.key.obj_id)
                inorder_traversal(node.right, result)
        
        result = []
        inorder_traversal(self.obj_tree.root, result)
        return result
