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

  # element : {url: String, count: Integer}
  def insert(self, element):
    
    ptr = self
    count = element['count']

    url = element['url']
    if count == 3100: 
      print(url)    
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
          break
        ptr = ptr.left
      else:
        if ptr.right == None:
          ptr.right = Tree(url, count)
          break     
        ptr = ptr.right


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