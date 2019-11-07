class TreeNode:
    def __init__(self, subset_size, hash_number, pointer):
        self.hash_number = hash_number
        self.level = subset_size
        self.children = []
        self.is_leaf = False
        self.pointer = pointer
        self.item_sets = set()

    def build_complete_tree(self):
        if self.level == 0:
            self.is_leaf = True
            return None

        for x in range(0, self.hash_number):
            temp_node = TreeNode(subset_size=self.level - 1, hash_number=self.hash_number, pointer=self.pointer + 1)
            self.children.append(temp_node)

        for children in self.children:
            children.build_complete_tree()

    def insert(self, candidate):
        if self.is_leaf:
            self.item_sets.add(frozenset(candidate))
            return

        hash_value = int(candidate[self.pointer]) % self.hash_number
        next_node = self.children[hash_value]
        next_node.insert(candidate)

    def contains(self, candidate):
        if self.is_leaf:
            if frozenset(candidate) in self.item_sets:
                return True
            else:
                return False

        hash_value = int(candidate[self.pointer]) % self.hash_number
        next_node = self.children[hash_value]
        return next_node.contains(candidate)


# if __name__ == '__main__':
#     x = TreeNode(3, 3, 0)
#     x.build_complete_tree()
#     var = [[1, 4, 5], [1, 2, 4], [4, 5, 7], [1, 2, 5], [4,5, 8], [1, 5, 9], [1, 3, 6], [2, 3, 4], [5, 6, 7], [3, 4, 5], [3, 5, 6], [3,5,7], [6, 8, 9], [3, 6, 7], [3, 6, 8]]
#     # var = [[1, 4, 5], [1, 2, 4], [3, 6, 8]]
#     for y in var:
#         x.insert(y)
#     print(x.contains([1, 2, 3]))
