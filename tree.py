class BlackPinkNode:
    def __init__(self, the_element, left=None, right=None, color=1):
        self.left = left
        self.right = right
        self.element = the_element
        self.color = color


class BPTree:
    def __init__(self, neg_inf):
        self.header = BlackPinkNode(neg_inf)
        self.header.left = self.header.right = BPTree.null_node

    null_node = BlackPinkNode(0)
    null_node.left = null_node.right = null_node

    BLACK = 1
    PINK = 0

    def is_empty(self):
        return self.header.right == BPTree.null_node

    def make_empty(self):
        self.header.right = BPTree.null_node

    def insert(self, item):
        self.current = self.parent = self.grand = self.header
        BPTree.null_node.element = item

        while self.current.element != item:
            self.great = self.grand
            self.grand = self.parent
            self.parent = self.current
            self.current = (
                self.current.left if item < self.current.element else self.current.right
            )

            if (
                self.current.left.color == BPTree.PINK
                and self.current.right.color == BPTree.PINK
            ):
                self.handle_reorient(item)

        if self.current != BPTree.null_node:
            return

        self.current = BlackPinkNode(item, BPTree.null_node, BPTree.null_node)

        if item < self.parent.element:
            self.parent.left = self.current
        else:
            self.parent.right = self.current

        self.handle_reorient(item)

    def handle_reorient(self, item):
        self.current.color = BPTree.PINK
        self.current.left.color = BPTree.BLACK
        self.current.right.color = BPTree.BLACK

        if self.parent.color == BPTree.PINK:
            self.grand.color = BPTree.PINK
            if item < self.grand.element != item < self.parent.element:
                self.parent = self.rotate(item, self.grand)
            self.current = self.rotate(item, self.great)
            self.current.color = BPTree.BLACK

        self.header.right.color = BPTree.BLACK

    def rotate(self, item, parent):
        if item < parent.element:
            return (
                parent.left
                if item < parent.left.element
                else self.rotate_with_right_child(parent.left)
            )
        else:
            return (
                parent.right
                if item < parent.right.element
                else self.rotate_with_right_child(parent.right)
            )

    def rotate_with_left_child(self, k2):
        k1 = k2.left
        k2.left = k1.right
        k1.right = k2
        return k1

    def rotate_with_right_child(self, k1):
        k2 = k1.right
        k1.right = k2.left
        k2.left = k1
        return k2

    def count_nodes(self):
        return self.count_nodes_helper(self.header.right)

    def count_nodes_helper(self, r):
        if r == BPTree.null_node:
            return 0
        else:
            l = 1
            l += self.count_nodes_helper(r.left)
            l += self.count_nodes_helper(r.right)
            return l

    def search(self, val):
        return self.search_helper(self.header.right, val)

    def search_helper(self, r, val):
        found = False
        while r != BPTree.null_node and not found:
            rval = r.element
            if val < rval:
                r = r.left
            elif val > rval:
                r = r.right
            else:
                found = True
                break
            found = self.search_helper(r, val)
        return found

    def inorder(self):
        self.inorder_helper(self.header.right)

    def inorder_helper(self, r):
        if r != BPTree.null_node:
            self.inorder_helper(r.left)
            c = 'B' if r.color == BPTree.BLACK else 'P'
            print(f"{r.element}{c}", end=" ")
            self.inorder_helper(r.right)

    def preorder(self):
        self.preorder_helper(self.header.right)

    def preorder_helper(self, r):
        if r != BPTree.null_node:
            c = 'B' if r.color == BPTree.BLACK else 'P'
            print(f"{r.element}{c}", end=" ")
            self.preorder_helper(r.left)
            self.preorder_helper(r.right)

    def postorder(self):
        self.postorder_helper(self.header.right)

    def postorder_helper(self, r):
        if r != BPTree.null_node:
            self.postorder_helper(r.left)
            self.postorder_helper(r.right)
            c = 'B' if r.color == BPTree.BLACK else 'P'
            print(f"{r.element}{c}", end=" ")

    def minimum(self):
        return self.find_minimum(self.header.right)

    def find_minimum(self, node):
        while node.left != BPTree.null_node:
            node = node.left
        return node.element

    def maximum(self):
        return self.find_maximum(self.header.right)

    def find_maximum(self, node):
        while node.right != BPTree.null_node:
            node = node.right
        return node.element

    def remove(self, item):
        self.header.right = self.remove_element(self.header.right, item)

    def remove_element(self, root, item):
        if root == BPTree.null_node:
            return root

        if item < root.element:
            root.left = self.remove_element(root.left, item)
        elif item > root.element:
            root.right = self.remove_element(root.right, item)
        else:
            if root.left == BPTree.null_node:
                return root.right
            elif root.right == BPTree.null_node:
                return root.left

            root.element = self.find_minimum(root.right)
            root.right = self.remove_element(root.right, root.element)

        return root


if __name__ == "__main__":
    bpt = BPTree(float("-inf"))

    print("Black Pink Tree Test\n")

    while True:
        print("\nBlack Pink Tree Operations\n")
        print("1. Insert")
        print("2. Search")
        print("3. Count nodes")
        print("4. Check empty")
        print("5. Clear tree")
        print("6. Minimum element")
        print("7. Maximum element")
        print("8. Remove element")
        print("Choose One: ", end="")
        choice = int(input())

        if choice == 1:
            print("Enter integer element to insert: ", end="")
            bpt.insert(int(input()))
        elif choice == 2:
            print("Enter integer element to search: ", end="")
            print("Search result:", bpt.search(int(input())))
        elif choice == 3:
            print("Nodes =", bpt.count_nodes())
        elif choice == 4:
            print("Empty status =", bpt.is_empty())
        elif choice == 5:
            print("\nTree Cleared")
            bpt.make_empty()
        elif choice == 6:
            print("Minimum element:", bpt.minimum())
        elif choice == 7:
            print("Maximum element:", bpt.maximum())
        elif choice == 8:
            print("Enter integer element to remove: ", end="")
            item_to_remove = int(input())
            bpt.remove(item_to_remove)
            print(f"Element {item_to_remove} removed from the tree.")
        else:
            print("Wrong Entry\n")

        print("\nPost order: ", end="")
        bpt.postorder()
        print("\nPre order: ", end="")
        bpt.preorder()
        print("\nIn order: ", end="")
        bpt.inorder()

        ch = input("\nDo you want to continue (Type y or n): ").lower()
        if ch != 'y':
            break