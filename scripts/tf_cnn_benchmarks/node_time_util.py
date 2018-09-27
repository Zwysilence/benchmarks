import os

from node import Node
from tensor import Tensor


def _simplify_device_name(device):
  """/job:localhost/replica:0/task:0/device:CPU:0 -> /cpu:0"""

  prefix1 = '/job:localhost/replica:0/task:0/device:'
  prefix2 = '/device:'
  # suffix = 'stream:'
  if device.startswith(prefix1):
    device = device[len(prefix1):]
  elif device.startswith(prefix2):
    device = device[len(prefix2):]

  # if device.endswith(suffix, 0, -2):
  #   device = 
  if '/' in device:
    device = '_'.join(device.split('/'))

  if ':' in device:
    device = '_'.join(device.split(':'))

  return device.lower()

def get_node_time(run_metadata):

  assert run_metadata != None
  assert hasattr(run_metadata, 'step_stats')
  assert hasattr(run_metadata.step_stats, 'dev_stats')

  dev_stats = run_metadata.step_stats.dev_stats
  for dev_stat in dev_stats:
    device_name = _simplify_device_name(dev_stat.device)

    # Ignore the node in CPU
    # if 'cpu' in device_name:
    #   continue
    extractNodeTime(device_name, dev_stat.node_stats)

  
def extractNodeTime(device_name, nodestats):
  # 
  # assert hasattr(nodestats, 'referenced_tensor')
  nodes = []
  out_dir = './graph/'

  if not os.path.exists(out_dir):
    os.mkdir(out_dir)

  minimum_start_time = nodestats[0].all_start_micros
  for node in nodestats:
    node_name = node.node_name
    all_start_micros = node.all_start_micros
    all_end_rel_micros = node.all_end_rel_micros

    if all_start_micros < minimum_start_time:
      minimum_start_time = all_start_micros

    d_node = Node(node_name, all_start_micros, all_end_rel_micros)

    for ref_tensor in node.referenced_tensor:
      tid = ref_tensor.allocation_id
      allocator_name = ref_tensor.allocator_name
      requested_bytes = ref_tensor.requested_bytes
      allocated_bytes = ref_tensor.allocated_bytes

      t = Tensor(d_node.node_name, tid=tid, 
                 requested_bytes=requested_bytes,
                 allocator_name=allocator_name,
                 allocated_bytes=allocated_bytes)
      d_node.ref_tensors.append(t)

    nodes.append(d_node)

  with open('%s%s.txt' % (out_dir, device_name), 'w') as fout:
    for node in nodes:
      assert (node.start_time >= minimum_start_time)
      node.start_time -= minimum_start_time
      node.end_time += node.start_time
      fout.write(node.node_name+' '+str(node.start_time)+' '+str(node.end_time)+'\n')

  with open("%s%s_refTensor.txt" % (out_dir, device_name), 'w') as fout:
    for node in nodes:
      fout.write(node.node_name+' ')
      for ref_tensor in node.ref_tensors:
        fout.write(str(ref_tensor.tid)+' ')
      fout.write('\n')