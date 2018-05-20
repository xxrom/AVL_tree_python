class Node(object):
  def __init__(self, data):
    self.data = data
    self.height = 0
    self.leftChild = None
    self.rightChild = None

class AVL(object):
  def __init__(self):
    self.root = None

  # проверяем валидность подДерева ()
  def settleViolation(self, data, node):
    balance = self.calcBalance(node)
    if balance > 1 and data < node.leftChild.data: # 1 case
      print('Left left heavy situation ...')
      return self.rotateRight(node)

    elif balance < -1 and data > node.rightChild.data: # 2 case
      print('Right right heavy situation ...')
      return self.rotateLeft(node)

    elif balance > 1 and data > node.leftChild.data: # 3 case ???
      print('Left right heavy situation ... ')
      node.leftChild = self.rotateLeft(node.leftChild)
      return self.rotateRight(node)

    elif balance < -1 and data < node.rightChild.data: # 4 case ???
      print('Right left heavy situation ...')
      node.rightChild = self.rotateRight(node.rightChild)
      return self.rotateLeft(node)

    print('subTree balanced =) ... %s ' % data)
    return node

  def insert(self, data):
    self.root = self.insertNode(data, self.root)
  ###
  def insertNode(self, data, node):
    if not node: # подДерево пустое
      return Node(data)

    if data < node.data: # обновляем либо левое/правое подДерево
      node.leftChild = self.insertNode(data, node.leftChild)
    else:
      node.rightChild = self.insertNode(data, node.rightChild)

    node.height = max( # обновляем высоту дерева
      self.calcHeight(node.leftChild),
      self.calcHeight(node.rightChild)) + 1

    return self.settleViolation(data, node) # проверяем валидность дерева
  ###
  def insertCheckBalanceTree(self, node):
    balance = self.calcBalance(node)
    if balance > 1 and self.calcBalance(node.leftChild) >= 0: # N1
      print('Left left heavy situation ...')
      return self.rotateRight(node) # 1

    elif balance < -1 and self.calcBalance(node.rightChild) < 0: # N2
      print('Right right heavy situation ...')
      return self.rotateLeft(node) # 1

    elif balance > 1 and self.calcBalance(node.leftChild) < 0: # N3
      print('Left right heavy situation ... ')
      node.leftChild = self.rotateLeft(node.leftChild) # 1
      return self.rotateRight(node) # 2

    elif balance < -1 and self.calcBalance(node.right) >= 0: # N4
      print('Right left heavy situation ...')
      node.rightChild = self.rotateRight(node.rightChild) # 1
      return self.rotateLeft(node) # 2

    print('subTree balanced =) ... %s ' % node.data)
    return node

  def remove(self, data):
    if self.root:
      self.root = self.removeNode(data, self.root)
  ###
  def removeNode(self, data, node):
    if not node:
      return None

    if data < node.data:
      node.leftChild = self.removeNode(data, node.leftChild)
    elif data > node.data:
      node.rightChild = self.removeNode(data, node.rightChild)
    else:
      # нашли node который нужно удалить
      if not node.rightChild and not node.leftChild: # когда лист
        print('Удаляем лист %s ' % node.data)
        del node
        return None

      elif node.rightChild and not node.leftChild: # есть только правый ребенок
        print('Удаляем node с правым ребенком %s ' % node.data)
        temp = node.rightChild
        del node
        return temp
      elif node.leftChild and not node.rightChild: # есть только левый ребенок
        print('Удаляем node с левым ребенком %s ' % node.data)
        temp = node.leftChild
        del node
        return temp

      print('Удаляем node с двумя детьми %s ' % node.data)
      minNode = self.getMinNode(node.rightChild)
      node.data = minNode.data
      node.rightChild = self.removeNode(minNode.data, node.rightChild)

    # теперь нужно отбалансировать дерево, где удалили
    node.height = max(
      self.calcHeight(node.leftChild),
      self.calcHeight(node.rightChild)) + 1

    return self.insertCheckBalanceTree(node) # балансируем дерево
  ###
  def getMinNode(self, node):
    if node.leftChild:
      return self.getMinNode(node.leftChild)

    return node # нашли минимум


  def calcHeight(self, node):
    if not node:
      return -1 # если ушли ниже листа, то высота -1

    return node.height

  # if it return value >  1 => left heavy tree --> right rotation
  # if it return value < -1 => right heavy tree --> left rotation
  def calcBalance(self, node):
    if not node:
      return 0 # почему тут ноль???  -1 - (-1) = 0, нет детей у него!

    return self.calcHeight(node.leftChild) - self.calcHeight(node.rightChild)

  # O(1)
  def rotateRight(self, node):
    print('Rotate to the right on node %s ' % node.data)

    # сохраняем левого ребенка и из него еще берем правого ребенка
    tempLeftChild = node.leftChild
    leftChild_rightChild = tempLeftChild.rightChild

    # левый ребенок node присваивает себе правым ребенком - родителя
    # node берет левого ребенка из правого ребенка (левого ребенка node)
    tempLeftChild.rightChild = node
    node.leftChild = leftChild_rightChild

    # пересчитываем высоты для нового корня leftChild и
    # node (правого ребенка нового корня)
    tempLeftChild.height = max(
      self.calcHeight(tempLeftChild.leftChild),
      self.calcHeight(tempLeftChild.rightChild)) + 1
    node.height = max(
      self.calcHeight(node.leftChild),
      self.calcHeight(node.rightChild)) + 1

    # вернем новый корень подДерева
    return tempLeftChild
  ###
  # O(1)
  def rotateLeft(self, node):
    print('Rotate to the left on node %s ' % node.data)

    # сохраняем правого ребенка и из него еще берем левого ребенка
    tempRightChild = node.rightChild
    rightChild_leftChild = tempRightChild.leftChild

    # правый ребенок node присваивает себе левым ребенком - родителя
    # node берет левого ребенка из правого ребенка (левого ребенка node)
    tempRightChild.leftChild = node
    node.rightChild = rightChild_leftChild

    # пересчитываем высоты для нового корня leftChild и
    # node (правого ребенка нового корня)
    tempRightChild.height = max(
      self.calcHeight(tempRightChild.leftChild),
      self.calcHeight(tempRightChild.rightChild)) + 1
    node.height = max(
      self.calcHeight(node.leftChild),
      self.calcHeight(node.rightChild)) + 1

    # вернем новый корень подДерева
    return tempRightChild

  # O(N)
  def traverse(self):
    print('traverse')
    if self.root:
      self.traverseInOrder(self.root)
  ### вывод: левый - корень - правый
  def traverseInOrder(self, node):
    if node.leftChild: # != None
      self.traverseInOrder(node.leftChild)

    print(' -> %s ' % node.data)

    if node.rightChild: #  != None
      self.traverseInOrder(node.rightChild)


# avl = AVL()
# avl.insert(10)
# avl.insert(20)
# avl.insert(30)
# avl.traverse() # right right heavy situation 10 <- 20 -> 30


# avl2 = AVL()
# avl2.insert(5)
# avl2.insert(3)
# avl2.insert(2)
# avl2.traverse() # left left heavy situation 2 <- 3 -> 5


# avl3 = AVL()
# avl3.insert(5)
# avl3.insert(3)
# avl3.insert(4)
# avl3.traverse() # left right heavy situation 3 <- 4 -> 5


# avl3 = AVL()
# avl3.insert(50)
# avl3.insert(60)
# avl3.insert(55)
# avl3.traverse() # right left heavy situation 50 <- 55 -> 60

avl4 = AVL()
avl4.insert(10)
avl4.insert(20)
avl4.insert(5)
avl4.insert(6)
avl4.insert(15)
avl4.traverse()

avl4.remove(15)
avl4.remove(20)
avl4.traverse()