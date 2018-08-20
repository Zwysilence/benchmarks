import sys
import os

# Process the metalog file
class ProcessFile():
  def __init__(self):
    # self.total_length = 100
    self.counts = dict()
    self.prev_value = dict()
    self.all_layers = ['conv', 'pool', 'affine','dropout', 'batchnorm', 'lrn']


  def calculate_max_variation(self, prev, curr):
    # assert(len(prev) == self.total_length)
    # assert(len(curr) == self.total_length)

    max_variation = 0
    length = len(prev)
    for i in range(length):
      v = abs(curr[i] - prev[i])
      if v > max_variation:
        max_variation = v

    return max_variation

  def calculate_all_variation(self, prev, curr):
    # assert(len(prev) == self.total_length)
    # assert(len(curr) == self.total_length)

    variation = []
    length = len(prev)
    for i in range(length):
      v = curr[i] - prev[i]
      variation.append(v)
      
    return variation


  def extract_value(self, tmp_value, dest):
    for v in tmp_value:
      if '[' in v:
        v = v.split('[')
        for vv in v:
          if vv == '':
            pass
          else:
            vv = vv.strip('[]')
            dest.append(float(vv))
      else:
        dest.append(float(v))

  def process_max(self, in_p, out_dir=None):
    return self.process_file(in_p=in_p,
                             func=self.calculate_max_variation,
                             out_dir=out_dir)

  def process_all(self, in_p, out_dir=None):
    return self.process_file(in_p=in_p,
                             func=self.calculate_all_variation,
                             out_dir=out_dir)

  def process_file(self,
                   in_p,
                   func,
                   out_dir=None
                   ):
    lines = in_p.readlines()

    for line in lines:
      flag = False
      for l in self.all_layers:
        if l in line:
          if 'images/sec' not in line:  # HACK for the last line
            flag = True

      if flag:
        curr_value = []
        layer_name = line.split('=')[0]
        if self.counts.get(layer_name) != None:
          self.counts[layer_name] += 1
        else:
          self.counts[layer_name] = 1

        tmp = line.split('=')[1]
        tmp = tmp.strip('[.]\n')
        # tmp = tmp[start:end]
        tmp_value = tmp.split(' ')

        if self.counts[layer_name] == 1:
          self.prev_value[layer_name] = []
          self.extract_value(tmp_value, self.prev_value[layer_name])

        else:
          self.extract_value(tmp_value, curr_value)

          variation = func(self.prev_value[layer_name], curr_value)
          self.prev_value[layer_name] = []
          self.prev_value[layer_name].extend(curr_value)
          if out_dir:
            if isinstance(variation, float):
              with open(out_dir+layer_name+'.txt', 'a') as out_p:
                out_p.write(str(variation) + '\n')
            elif isinstance(variation, list):
              with open(out_dir+layer_name+'_'+str(self.counts[layer_name]-1)+'.txt', 'a') as out_p:
                for v in variation:
                 out_p.write(str(v) + '\n')
          else:
            pass
            # print("[%s] The max variation between %d and %d is %f" % (layer_name, self.counts[layer_name] - 1, self.counts[layer_name], variance))

    in_p.close()

def main():
  pf = ProcessFile()
  if len(sys.argv) == 1:
    print("Error: need input file at least!")

  filename = sys.argv[1]
  out_dir = None

  if len(sys.argv) == 3:
    out_dir = sys.argv[2]

  in_p = open(filename)
  pf.process_file(in_p, out_dir)


if __name__ == '__main__':
  main()
