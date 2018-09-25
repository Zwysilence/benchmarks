

class Node():
  def __init__(self,
               node_name,
               start_time,
               end_time):
    self.node_name = node_name

    # Can be delayed due to other operation. such as swap in
    self.logic_time = 0

    # Init by the run_metadata
    self.start_time = start_time
    self.end_time = end_time

    self.pending_count = -1
    self.fanout_nodes = []

  def __cmp__(self, other):
    if self.pending_count == other.pending_count:
      return self.start_time < other.start_time

    return self.pending_count < self.pending_count
