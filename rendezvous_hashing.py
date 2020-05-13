from hashlib import md5

class rendezvous_hashing():
  
  def __init__(self, nodes):
    assert len(nodes) > 0
    self.nodes = nodes

  def get_weight(self, key, node):
    hashed_key = int(md5(key.encode()).hexdigest(), 16)
    node_string = node.host + ":" +str(node.port)
    hashed_node = int(md5(node_string.encode()).hexdigest(), 16)
    return ((hashed_node  ^ hashed_key) % (2 ^ 31))

  def get_node(self, key):
    highest_weight = 0
    the_node = None
    for node in self.nodes:
      weight = self.get_weight(key, node)
      # print('Node at {}:{}'.format(node.host, node.port))
      # print("has weight {} for key {}".format(weight, key))
      if weight > highest_weight:
        highest_weight = weight
        the_node = node
    return the_node