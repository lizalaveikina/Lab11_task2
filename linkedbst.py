"""
File: linkedbst.py
Author: Ken Lambert
"""
import time

from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
from math import log


from sys import setrecursionlimit

setrecursionlimit(10**6)


class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            s = ""
            if node != None:
                s += recurse(node.right, level + 1)
                s += "| " * level
                s += str(node.data) + "\n"
                s += recurse(node.left, level + 1)
            return s

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right != None:
                    stack.push(node.right)
                if node.left != None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""

        def recurse(node):
            if node is None:
                return None
            elif item == node.data:
                return node.data
            elif item < node.data:
                return recurse(node.left)
            else:
                return recurse(node.right)

        return recurse(self._root)

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""

        # Helper function to search for item's position
        def recurse(node):
            # New item is less, go left until spot is found
            if item < node.data:
                if node.left == None:
                    node.left = BSTNode(item)
                else:
                    recurse(node.left)
            # New item is greater or equal,
            # go right until spot is found
            elif node.right == None:
                node.right = BSTNode(item)
            else:
                recurse(node.right)
                # End of recurse

        # Tree is empty, so new item goes at the root
        if self.isEmpty():
            self._root = BSTNode(item)
        # Otherwise, search for the item's spot
        else:
            recurse(self._root)
        self._size += 1

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree." "")

        # Helper function to adjust placement of an item
        def liftMaxInLeftSubtreeToTop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            currentNode = top.left
            while not currentNode.right == None:
                parent = currentNode
                currentNode = currentNode.right
            top.data = currentNode.data
            if parent == top:
                top.left = currentNode.left
            else:
                parent.right = currentNode.left

        # Begin main part of the method
        if self.isEmpty():
            return None

        # Attempt to locate the node containing the item
        itemRemoved = None
        preRoot = BSTNode(None)
        preRoot.left = self._root
        parent = preRoot
        direction = "L"
        currentNode = self._root
        while not currentNode == None:
            if currentNode.data == item:
                itemRemoved = currentNode.data
                break
            parent = currentNode
            if currentNode.data > item:
                direction = "L"
                currentNode = currentNode.left
            else:
                direction = "R"
                currentNode = currentNode.right

        # Return None if the item is absent
        if itemRemoved == None:
            return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not currentNode.left == None and not currentNode.right == None:
            liftMaxInLeftSubtreeToTop(currentNode)
        else:

            # Case 2: The node has no left child
            if currentNode.left == None:
                newChild = currentNode.right

                # Case 3: The node has no right child
            else:
                newChild = currentNode.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == "L":
                parent.left = newChild
            else:
                parent.right = newChild

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = preRoot.left
        return itemRemoved

    def replace(self, item, newItem):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe != None:
            if probe.data == item:
                oldData = probe.data
                probe.data = newItem
                return oldData
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        """
        Return the height of tree
        :return: int
        """

        def height1(top):
            """
            Helper function
            :param top:
            :return: int
            """

            if top is not None:
                return max(height1(top.left), height1(top.right)) + 1
            return -1

        return height1(self._root)

    def is_balanced(self):
        """
        Return True if tree is balanced
        :return: bool
        """
        length = self._size
        return self.height() < 2 * log((length + 1), 2) - 1

    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        list_of_the_items_in_the_tree = sorted(
            item for item in self if low <= item <= high
        )
        return list_of_the_items_in_the_tree

    def rebalance(self):
        """
        Rebalances the tree.
        :return: None
        """
        nodes = sorted(self.inorder())

        def list2tree(root, node_list):
            """
            Функція переведення відсортованого спуску у збалансовану форму
            """
            length = len(node_list)
            if length == 0:
                return None
            root.data = node_list[length // 2]
            root.left = list2tree(BSTNode(None), node_list[: length // 2])
            root.right = list2tree(BSTNode(None), node_list[length // 2 + 1 :])
            return root

        self._root = list2tree(self, nodes)
        return self

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        items = sorted((i for i in self.inorder()), reverse=True)
        for i in range(len(items)):
            if items[i] <= item:
                if i > 0:
                    return items[i - 1]
                else:
                    return None
        return items[-1]


    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """

        items = sorted(i for i in self.inorder())
        for i in range(len(items)):
            if items[i] >= item:
                if i > 0:
                    return items[i - 1]
                else:
                    return None
        return items[-1]


    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param path:
        :type path:
        :return:
        :rtype:
        """

        def read_words(filename):
            with open(filename, "r", encoding="utf-8") as file:
                return [line.strip() for line in file.readlines()]

        words = read_words("words.txt")
        random_words = [word for word in set(words)]
        search_words = list(set(random_words))[:40000:4]
        print(
            "1. Час пошуку 10000 випадкових слів у впорядкованому за абеткою словнику\n"
            "(пошук у списку слів з використанням методів вбудованого типу list)."
        )
        start_time = time.perf_counter()
        for word in search_words:
            # word in words
            words.index(word)
        print(time.perf_counter() - start_time)

        tree = LinkedBST(words)
        print(
            "2. Час пошуку 10000 випадкових слів у словнику, який представлений у вигляді\n"
            "бінарного дерева пошуку. Бінарне дерево пошуку будується на основі посліддовного\n"
            "додавання в дерево слів зі словника який впорядкований за абеткою. "
        )
        start_time = time.perf_counter()
        for word in search_words:
            tree.find(word)
        print(time.perf_counter() - start_time)

        print(
            "3. Час пошуку 10000 випадкових слів у словнику, який представлений у вигляді\n"
            "бінарного дерева пошуку. Бінарне дерево пошуку будується на основі посліддовного\n"
            "додавання в дерево слів зі словника який не впорядкований за абеткою\n"
            "(слова в дерево додаються випадковим чином)."
        )

        tree_from_unordering_list = LinkedBST(random_words)
        start_time = time.perf_counter()
        for word in search_words:
            tree_from_unordering_list.find(word)
        print(time.perf_counter() - start_time)

        print(
            "4. пошуку 10000 випадкових слів у словнику, який представлений у вигляді збалансованого бінарного дерева пошуку."
        )
        if not tree_from_unordering_list.is_balanced():
            tree_from_unordering_list.rebalance()
        start_time = time.perf_counter()
        for word in search_words:
            tree_from_unordering_list.find(word)
        print(time.perf_counter() - start_time)


if __name__ == "__main__":
    # tree = LinkedBST()
    # tree.demo_bst("words.txt")
    # pass
    tree = LinkedBST(list(range(1, 11)) + list(range(15, 21)))
    # print("\nAdded 1..10:\n" + str(tree))

    # lyst = list(range(1, 16))
    # print(tree.is_balanced())
    # tree.rebalance()
    # print(tree)
    # print(tree.successor(5))
    # print(sorted(tree))
    print(tree.predecessor(2))
    print(tree.successor(20))