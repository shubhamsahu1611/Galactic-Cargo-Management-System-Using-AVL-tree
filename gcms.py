
from bin import Bin
from avl import AVLTree
from object import Object, Color
from exceptions import NoBinFoundException

class GCMS:
    def __init__(self):
        # Maintain all the Bins and Objects in GCMS
        #create bin and object avl tree
        def comp1(node1, node2):
            if node1.remaining_capacity < node2.remaining_capacity:
                return -1  # Go left
            elif node1.remaining_capacity > node2.remaining_capacity:
                return 1  # Go right
            else:
                # If remaining_capacity is the same, compare bin_id
                 # Smaller bin_id goes left
                if node1.bin_id < node2.bin_id:
                    return -1
                elif node1.bin_id > node2.bin_id:
                    return 1
                else:
                    return 0


        
        def comp2(node1, node2):
            # if node1 is None or node2 is None:
            #     return False
            # # If node1's object_id is less than node2's, it goes left
            # return node1.obj_id < node2.obj_id
            if node1.obj_id < node2.obj_id:
                return -1
            elif node1.obj_id > node2.obj_id:
                return 1
            else:
                return 0
        def comp3(node1, node2):
            if node1.bin_id < node2.bin_id:
                return -1
            elif node1.bin_id > node2.bin_id:
                return 1
            else:
                return 0
            # if node1 is None or node2 is None:
            #     return False
            # return node1.bin_id<node2.bin_id
        def comp4(node1, node2):
            if node1.remaining_capacity < node2.remaining_capacity:
                return -1
            elif node1.remaining_capacity > node2.remaining_capacity:
                return 1
            else:
                if node1.bin_id < node2.bin_id:
                   return 1
                elif node1.bin_id > node2.bin_id:
                    return -1
                else:
                    return 0
                    
        


        self.bin_tree_leastId=AVLTree(comp1)
        self.object_tree=AVLTree(comp2)
        self.id_bin=AVLTree(comp3)
        self.bin_tree_greatestId=AVLTree(comp4)
        pass 

    def add_bin(self, bin_id, capacity):
        new_bin=Bin(bin_id, capacity)
        new_bin2=Bin(bin_id, capacity)
        new_bin3=Bin(bin_id, capacity)
        self.bin_tree_leastId.insert(new_bin)
        self.bin_tree_greatestId.insert(new_bin2)
        self.id_bin.insert(new_bin3)
        pass
    
    def compactFit_With_LeastId(self, root, size):
        if root is None:
            return None
        ans=None
        # print(1)
        if root.key.remaining_capacity<size:
            return self.compactFit_With_LeastId(root.right, size)
        else:
            ans=root
            left_ans=self.compactFit_With_LeastId(root.left, size)
            if left_ans is None:
                return ans
            else :
                return left_ans
        
                
            # return left_ans if left_ans else root
    
    def compactFit_With_GreatestId(self, root, size):
        # print(2)
        if root is None:
            return None
        if root.key.remaining_capacity<size:
            return self.compactFit_With_GreatestId(root.right, size)
        else:
            left_ans=self.compactFit_With_GreatestId(root.left, size)
            return left_ans if left_ans else root

    def largestFit_With_LeastId(self, root, size):
        # print(3)
        if root is None:
            return None
        else:
            right_ans =  self.largestFit_With_LeastId(root.right, size)
            if right_ans:
                return right_ans
            else:
                if root.key.remaining_capacity >= size:
                    return root
                else:
                    return None

    def largestFit_With_GreatestId(self, root, size):
        # print(4)
        if root is None:
            return None
        
        else: 
            right_ans= self.largestFit_With_GreatestId(root.right, size)
            if right_ans is None and root.key.remaining_capacity>=size:
                return root
            else:
                return right_ans

    def find_bin(self, color, size):
        if color == Color.BLUE:
            return self.compactFit_With_LeastId(self.bin_tree_leastId.root, size)
        elif color == Color.YELLOW:
            return self.compactFit_With_GreatestId(self.bin_tree_greatestId.root, size)
        elif color == Color.RED:
            return self.largestFit_With_LeastId(self.bin_tree_greatestId.root, size)
        else:
            return self.largestFit_With_GreatestId(self.bin_tree_leastId.root, size)

    def add_object(self, object_id, size, color):
        def find_bin_to_add_obj(root, bin_id):
            if root == None:
                return None
            if root.key.bin_id == bin_id:
                return root
            elif root.key.bin_id < bin_id:
                return find_bin_to_add_obj(root.right, bin_id)
            else:
                return find_bin_to_add_obj(root.left, bin_id)
        suitable_bin=self.find_bin(color, size)
        if suitable_bin is None:
            raise NoBinFoundException
        else:
            id=suitable_bin.key.bin_id
            my_obj=Object(object_id, size , color, id)
            new_cap=suitable_bin.key.remaining_capacity - size
            self.object_tree.insert(my_obj)
            temp_bin=Bin(id, new_cap+size)
            temp_bin2=Bin(id, new_cap+size)
            new_bin=Bin(id, new_cap)


            #update node in id_bin tree
            myNode=find_bin_to_add_obj(self.id_bin.root, id)
            myNode.key.obj_tree.insert(my_obj)
            myNode.key.remaining_capacity-=size
            
            #updating least and greatest id tree   
            self.bin_tree_greatestId.delete(temp_bin)
            self.bin_tree_leastId.delete(temp_bin2)

            self.bin_tree_greatestId.insert(new_bin)
            self.bin_tree_leastId.insert(new_bin)

            new_bin=Bin(id, new_cap)
            self.bin_tree_leastId.insert(new_bin)
            self.bin_tree_greatestId.insert(new_bin)
           
    def find_object(self, obj_id):
        def search_util(root, obj_id):
            if root is None:
                return None
            
            # Assuming each node contains a tuple where the first element is the Object # root.key is a tuple (Object, parent_bin)
            
            if root.key.obj_id == obj_id:
                return root
            
            # If object_id is smaller, search in the left subtree
            if obj_id < root.key.obj_id:
                return search_util(root.left, obj_id)
            # If object_id is greater, search in the right subtree
            else:
                return search_util(root.right, obj_id)
        
        # Start the recursive search from the root of obj_tree
        return search_util(self.object_tree.root, obj_id)
        
    def delete_object(self, object_id):

        myObject = self.find_object(object_id)
        if myObject is None :
            return None
        temp=myObject.key
        size=myObject.key.size
        parent_id=myObject.key.parent_id
        self.object_tree.delete(myObject.key)

        def search_util(root, bin_id):
            if root is None:
                return None
            if root.key.bin_id == bin_id:
                return root
            if bin_id < root.key.bin_id:
                return search_util(root.left, bin_id)
            return search_util(root.right, bin_id)
        bin=search_util(self.id_bin.root, parent_id) #from bin_id tree
        cap=bin.key.remaining_capacity
        
        #now we find the obj in the bin insie tree and delte it using the av=bove algo only 
        bin.key.obj_tree.delete(temp)
        bin.key.remaining_capacity+=size
        
        temp_bin1=Bin(parent_id , cap)
        temp_bin2=Bin(parent_id , cap)

        self.bin_tree_greatestId.delete(temp_bin1)
        self.bin_tree_leastId.delete(temp_bin2)
        
        new_bin1=Bin(parent_id , cap+size)
        new_bin2=Bin(parent_id , cap+size)

        self.bin_tree_greatestId.insert(new_bin1)
        self.bin_tree_leastId.insert(new_bin2)

    def bin_info(self, bin_id):
        def search_util(root, bin_id):
            if root is None:
                return None
            if root.key.bin_id == bin_id:
                return root
            if bin_id < root.key.bin_id:
                return search_util(root.left, bin_id)
            return search_util(root.right, bin_id)

        bin_node = search_util(self.id_bin.root, bin_id)
        if bin_node:
            return ((bin_node.key.remaining_capacity,  bin_node.key.objects_list()))
        return None

    def object_info(self, object_id):
        myObj = self.find_object(object_id)
        if myObj is None:
            return None
        else:
            return myObj.key.parent_id
        
    
