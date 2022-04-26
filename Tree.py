class Tree:

  # noeuds gauches => decroissants
  # noeuds droits => croissants
  def __init__(self, url = None, count = None):
      self.height = 0
      self.parent = None
      self.value = count
      self.left = None
      self.right = None
      self.urls = []
      if url != None:
        self.urls.append(url)
      pass
 

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
      root.height = root.getHeight()
      root.parent.height = root.parent.getHeight()    
      if parent != None:
        if (parent.left != None and parent.left.value == root.value):
          parent.addLeftNode(root.parent)
        else:
          parent.addRightNode(root.parent)
        parent.height = parent.getHeight()
      else:
        root.parent.parent = None


  def rightRotate(self):
    root = self
    parent = root.parent
    if root.left != None:
      save = root.left.right
      root.left.addRightNode(root) 
      root.addLeftNode(save)
      root.height = root.getHeight()
      root.parent.height = root.parent.getHeight()
      if parent != None:
        if parent.left != None and parent.left.value == root.value:
          parent.addLeftNode(root.parent)
        else:
          parent.addRightNode(root.parent)
        parent.height = parent.getHeight()
      else:
        root.parent.parent = None

  # element : {url: String, count: Integer}
  def insert(self, element):
    #print('begin of insertion')
    temp = self
    ptr = self
    count = element['count']

    url = element['url']
    if ptr.value == None:
      ptr.urls.append(url)
      ptr.value = count
      return ptr
    
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

    ptr.height = ptr.getHeight()
    while ptr.parent != None:
      ptr = ptr.parent
      ptr.height = ptr.getHeight()
      bf = ptr.getBf()
      if abs(bf) == 2:
        #print('arbre non-equilibré', ptr.value, count, ptr.value)
        if ptr.left != None and count < ptr.value:
          if count > ptr.left.value:
            ptr.left.leftRotate()
            ptr.rightRotate()
          elif count < ptr.left.value:
            ptr.rightRotate()
        if ptr.right != None and count > ptr.value:
          if count > ptr.right.value:
            ptr.leftRotate()            
          elif count < ptr.right.value:
            ptr.right.rightRotate()
            ptr.leftRotate()
        break
      elif bf == 0:
        break

    while temp.parent != None:
      temp = temp.parent
    return temp

  def getHeight(self):
    root = self
    if root.left == None and root.right == None:
      return 0
    left = 0
    right = 0
    if root.left != None:
      left = 1 + root.left.height
    if root.right != None:
      right = 1 + root.right.height

    return max([left, right])

  def getBf(self):
    root = self
    left = 0
    right = 0
    if root.left:
      left = 1 + root.left.height
    if root.right:
      right = 1 +root.right.height

    return abs(right - left)
  def descendingSort(self, size):
    offset = 0
    ptr = self
    value = ptr.value
    if value == None:
      return ptr
    while True:
      if ptr.right == None:
        break
      ptr = ptr.right
    out = []
    while ptr != None and offset < size:
      if (ptr.left and ptr.left.value == value) or (ptr.right and ptr.right.value == value):
        break
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