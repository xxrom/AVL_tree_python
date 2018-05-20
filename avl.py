class Node(object):
  def __init__(self, data):
    self.data = data
    self.height = 0
    self.leftChild = None
    self.rightChild = None

class AVL(object):
  def __init__(self):
    self.root = None

  def calcHeight(self, node):
    if not node:
      return -1 # если ушли ниже листа, то высота -1

    return node.height

  # if it return value >  1 => left heavy tree --> right rotation
  # if it return value < -1 => right heavy tree --> left rotation
  def calcBalance(self, node):
    if not node:
      return 0
    return self.calcHeight(node.leftChild) - self.calcHeight(node.rightChild)