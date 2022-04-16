from Tree import * 

tree = Tree()

tree.insert({'count':10, 'url': 'a'})
tree.insert({'count':3, 'url': 'a'})
tree.insert({'count':1, 'url': 'a'})
tree.insert({'count':6, 'url': 'a'})
tree.insert({'count':4, 'url': 'a'})
tree.insert({'count':9, 'url': 'a'})
tree.insert({'count':8, 'url': 'a'})
tree.insert({'count':5, 'url': 'a'})

tree.left.rightRotate()
print(tree.getHeight())

