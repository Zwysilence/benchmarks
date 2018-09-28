
class Tensor():
  def __init__(self,
               node_name,
               tid=0,
               dtype=None,
               requested_bytes=0,
               allocator_name=None,
               allocated_bytes=0):
    self.node_name = node_name
    self.tid = tid

    self.dtype = dtype

    self.allocator_name = allocator_name
    self.requested_bytes = requested_bytes
    self.allocated_bytes = allocated_bytes

  def name(self):
    return self.node_name+'_'+str(self.tid)