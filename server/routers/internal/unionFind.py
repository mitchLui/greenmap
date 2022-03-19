class UnionFind:

    tree = {}

    def __init__(self, stuff):
        self.tree = {}
        for thing in stuff:
            self.tree[thing] = thing

    def find(self, x):
        if self.tree[x] == x:
            return x, 0
        root, depth = self.find(self.tree[x])
        return root, depth + 1

    def union(self, a, b):
        x, d1 = self.find(a)
        y, d2 = self.find(b)
        if d1 > d2:
            self.tree[y] = x
        else:
            self.tree[x] = y

    def getGroups(self):
        groups = {}
        for node in self.tree:
            root = self.find(node)
            if root in groups:
                groups[root].append(node)
            else:
                groups[root] = [node]
        return groups.values()