from hashlib import md5
import bisect

class consistent_hashing():

  def __init__(self, nodes, replicas=2):
    assert len(nodes) > 0
    self.nodes = nodes
    self.replicas = replicas
    self.key = []
    self.ring = {}

  def get_replicas(self, node):
    hashed = []
    for i in range(self.replicas):
      node_string = node.host + ":" +str(node.port)+":"+str(i)
      hashed_node = int(md5(node_string.encode()).hexdigest(), 16)
      hashed.append(hashed_node)
    return hashed

  def get_virtual_node(self, node):
    for hash in self.get_replicas(node):
      self.ring[hash] = node
      bisect.insort(self.key, hash)

  def generate_node_ring(self):
    for node in self.nodes:
      self.get_virtual_node(node)

  def get_node(self, key):
    hashed_key = int(md5(key.encode()).hexdigest(), 16)
    location = bisect.bisect(self.key, hashed_key)
    if location == len(self.key):
      location = 0
    return self.ring[self.key[location]]
  
  def delete_node(self, node):
    for hash in self.get_replicas(node):
      del self.ring[hash]
      index = bisect.bisect_left(self.key, hash)
      del self.key[index]

  