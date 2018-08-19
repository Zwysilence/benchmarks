import sys
import os

class ProcessFile():
  def __init__(self):
    self.total_length = 100
    self.counts = dict()
    self.prev_value = dict()
    self.all_layers = ['conv', 'pool', 'affine','dropout', 'batchnorm', 'lrn']


  def calculate_variance(self, prev, curr):
    # assert(len(prev) == self.total_length)
    # assert(len(curr) == self.total_length)

    max_variance = 0
    for i in range(self.total_length):
      v = abs(curr[i] - prev[i])
      if v > max_variance:
        max_variance = v

    return max_variance

  def extract_value(self, tmp_value, dest):
    for v in tmp_value:
      if '[' in v:
        v = v.split('[')
        for vv in v:
          if vv == '':
            pass
          else:
            vv = vv.split('[]')
            dest.append(float(vv))
      else:
        dest.append(float(vv))


  def process_file(self, in_p, out_dir=None):
    lines = in_p.readlines()

    for line in lines:
      flag = False
      for l in self.all_layers:
        if l in line:
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
          # for v in tmp_value:
          #   if '[' in v:
          #     v = v.split('[')
          #     for vv in v:
          #       if vv = '':
          #         pass
          #       else:
          #         vv = vv.split('[]')
          #         self.prev_value[layer_name].append(float(vv))
          #   else:
          #     self.prev_value[layer_name].append(float(v))
        else:
          self.extract_value(tmp_value, curr_value)
          # for v in tmp_value:
          #   curr_value.append(float(v))

          variance = self.calculate_variance(self.prev_value[layer_name], curr_value)
          self.prev_value[layer_name] = []
          self.prev_value[layer_name].extend(curr_value)
          if out_dir:
            with open(out_dir+layer_name+'.txt', 'a') as out_p:
              out_p.write(str(variance) + '\n')
          else:
            print("[%s] The max variance between %d and %d is %f" % (layer_name, self.counts[layer_name] - 1, self.counts[layer_name], variance))

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
