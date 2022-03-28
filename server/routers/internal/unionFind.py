import math

class UnionFind:

    def __init__(self, stuff):
        self.tree = {}
        for thing in stuff:
            self.tree[thing] = thing

    def find(self, x):
        if self.tree[x] == x:
            return x, 0
        root, depth = self.find(self.tree[x])
        self.tree[x] = root
        return root, 1

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

if __name__ == "__main__":
    data = [1,3,4,5,6,7,8,9,12,13,14,15,17]
    uf = UnionFind(data)
    for i in range(len(data)):
        for j in range(i + 1, len(data)):
            a = data[i]
            b = data[j]
            if abs(a - b) <= 1:
                uf.union(a, b)
    print(uf.getGroups())