from Tree import * 

tree = Tree()

tree.insert({'count':8, 'url': 'a'})
tree.insert({'count':3, 'url': 'a'})
tree.insert({'count':1, 'url': 'a'})
tree.insert({'count':8, 'url': 'a'})
tree.insert({'count':6, 'url': 'a'})
tree.insert({'count':4, 'url': 'a'})
tree.insert({'count':7, 'url': 'a'})

print(tree.value)
print(tree.left.value)
print(tree.left.left.value)
print(tree.left.right.value)
print(tree.left.right.left.value)
print(tree.left.right.right.value)