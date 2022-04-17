class Tree:

  # noeuds gauches => decroissants
  # noeuds droits => croissants
  def __init__(self, url = None, count = None):
      self.parent = None
      self.value = count
      self.left = None
      self.right = None
      self.urls = []
      if url != None:
        self.urls.append(url)
      pass

  def __str__(self):
      return str(self.value)

 

  def addRightNode(self, node):
    self.right = node
    if node != None:
      node.parent = self

  def addLeftNode(self, node):
    self.left = node
    if node != None:
      node.parent = self

  def leftRotate(self):
    root = self
    parent = root.parent
    if root.right != None:
      save = root.right.left
      root.right.addLeftNode(root) 
      root.addRightNode(save)
      if parent != None:
        if (parent.left.value == root.value):
          parent.addLeftNode(root.parent)
        else:
          parent.addRightNode(root.parent)
      else:
        root.parent.parent = None

  def rightRotate(self):
    root = self
    parent = root.parent
    if root.left != None:
      save = root.left.right
      root.left.addRightNode(root) 
      root.addLeftNode(save)
      if parent != None:
        if parent.left != None and parent.left.value == root.value:
          parent.addLeftNode(root.parent)
        else:
          parent.addRightNode(root.parent)
      else:
        root.parent.parent = None


   
  # element : {url: String, count: Integer}
  def insert(self, element):
    
    ptr = self
    count = element['count']

    url = element['url']
    if ptr.value == None:
      ptr.urls.append(url)
      ptr.value = count
      return
    
    while True:
      if count == ptr.value:
        ptr.urls.append(url)
        break
      elif count < ptr.value :
        if ptr.left == None:
          ptr.left = Tree(url, count)
          ptr.left.parent = ptr
          break
        ptr = ptr.left
      else:
        if ptr.right == None:
          ptr.right = Tree(url, count)
          ptr.right.parent = ptr       
          break     
        ptr = ptr.right
    child = None
    if ptr.right.value == count:
      child = ptr.right
    else:
      child = ptr.left
    if not ptr.isAvl(2, child):
      print('arbre non-equilibré')

  def isAvl(self, depth, child):
    root = self
    height = 0
    if root.right != None and root.right.value == child.value:
      if root.left != None:
        height = root.left.getHeight()
    else:
      if root.right != None:
        height = root.right.getHeight()
    print(depth, height)

    if abs(depth - height) > 2: 
      return False
    return True

  def getHeight(self):
    root = self
    if root.left == None and root.right == None:
      return 0
    left = 0
    right = 0
    if root.left != None:
      left = 1 + root.left.getHeight()
    if root.right != None:
      right = 1 + root.right.getHeight()

    return max([left, right])

  def descendingSort(self, size):
    offset = 0
    ptr = self
    if ptr.value == None:
      return ptr
    while True:
      if ptr.right == None:
        break
      parent = ptr
      ptr = ptr.right
      ptr.parent = parent
    out = []
    while ptr != None and offset < size:
      for url in ptr.urls:
        out.append({'query': url, 'count': ptr.value})
        offset+=1
        if offset >= size:
          return out
      if ptr.left != None:
        left_array =  ptr.left.descendingSort(size - offset)
        out += left_array
        offset += len(left_array)
      ptr = ptr.parent
    return out