import os

from node import Node
from tensor import Tensor

nodes = dict()
out_dir = './graph/'

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
    # if device_name == 'gpu_0':
    # time in 'gpu_0' contains the cpu time, not gpu computation time
    # 'gpu_0' contains the output info, but 'gpu_0_stream_all' don't
    if device_name == 'gpu_0_stream_all':
      # don't contain '_SOURCE' node
      extractNodeTime(device_name, dev_stat.node_stats)
    
    if device_name == 'gpu_0':
      assert len(nodes) > 0
      extractNodeTime(device_name, dev_stat.node_stats)
      extractTensor(device_name, dev_stat.node_stats)

  PrintResult()

def extractTensor(device_name, nodestats):
  for node_stat in nodestats:
    node_name = node_stat.node_name
    try:
      assert nodes.__contains__(node_name)
    except AssertionError:
      print("Error tensor: %s" % node_name)
      # exit(1)
      continue
    nodes[node_name].InitOutput(node_stat)
  
def extractNodeTime(device_name, nodestats):
  # 
  # assert hasattr(nodestats, 'referenced_tensor')
  

  if not os.path.exists(out_dir):
    os.mkdir(out_dir)

  for node_stat in nodestats:
    node_name = node_stat.node_name
    if ':' in node_name:
      node_name = node_name.split(':')[0]
    if device_name == 'gpu_0':
      if nodes.__contains__(node_name):
        continue
    if not nodes.__contains__(node_name):
      nodes[node_name] = Node(node_name)
    nodes[node_name].AddTime(node_stat)

def PrintResult():
  all_start_time = [node.start_time for node in nodes.values()]
  min_start_time = min(all_start_time)

  with open('%s%s_nodetime.txt' % (out_dir, 'gpu_0'), 'w') as fout:
    for node in nodes.values():
      assert (node.start_time >= min_start_time)
      node.start_rel_time = node.start_time - min_start_time
      node.end_time = node.start_rel_time + node.exec_time
      fout.write(node.node_name+' '+str(node.start_rel_time)+' '+str(node.end_time)+'\n')

  with open("%s%s_outputs.txt" % (out_dir, 'gpu_0'), 'w') as fout:
    for node in nodes.values():
      output_num = len(node.outputs)
      fout.write("SrcNode"+' '+node.node_name+' '+str(output_num)+'\n')
      for output in node.outputs.values():
        fout.write("Output"+' '+str(output.tid)+' '+
                   str(output.requested_bytes)+' '+
                   str(output.allocated_bytes)+' '+                   
                   str(output.allocator_name)+' '+
                   str(output.allocated_time)+'\n')

  # minimum_start_time = nodestats[0].all_start_micros
  # for node in nodestats:
  #   node_name = node.node_name
  #   all_start_micros = node.all_start_micros
  #   all_end_rel_micros = node.all_end_rel_micros

  #   if all_start_micros < minimum_start_time:
  #     minimum_start_time = all_start_micros

  #   d_node = Node(node_name, all_start_micros, all_end_rel_micros)

    # for ref_tensor in node.referenced_tensor:
    #   tid = ref_tensor.allocation_id
    #   allocator_name = ref_tensor.allocator_name
    #   requested_bytes = ref_tensor.requested_bytes
    #   allocated_bytes = ref_tensor.allocated_bytes

    #   t = Tensor(d_node.node_name, tid=tid, 
    #              requested_bytes=requested_bytes,
    #              allocator_name=allocator_name,
    #              allocated_bytes=allocated_bytes)
    #   d_node.ref_tensors.append(t)

    # for i in node.output:
    #   i_slot = i.slot
    #   td = i.tensor_description

    #   # dtype = td.dtype
    #   # dshape = td.shape
    #   allocation_d = td.allocation_description

    #   requested_bytes = allocation_d.requested_bytes
    #   allocated_bytes = allocation_d.allocated_bytes
    #   allocator_name = allocation_d.allocator_name

    #   t = Tensor(d_node.node_name, tid=i_slot,
    #              requested_bytes=requested_bytes,
    #              allocator_name=allocator_name,
    #              allocated_bytes=allocated_bytes,
    #              allocated_time=all_start_micros)

    #   d_node.outputs.append(t)

    # nodes.append(d_node)

  metadata_log = False
  if metadata_log:
    with open("%s%s_nodetime_metadata.txt" % (out_dir, device_name), 'w') as fout:
      for node in nodes:
        fout.write(node.node_name+' '+str(node.start_time)+' '+str(node.end_time)+'\n')


  
        # fout.write(str(output.dtype)+' '+str(output.tid)+' ')
      # for ref_tensor in node.ref_tensors:
      #   fout.write(str(ref_tensor.tid)+' ')
      # fout.write('\n')
