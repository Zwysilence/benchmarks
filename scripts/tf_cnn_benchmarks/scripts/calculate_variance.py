import sys
import os

total_length = 100

def calculate_variance(prev, curr):
  assert(len(prev) == total_length)
  assert(len(curr) == total_length)

  max_variance = 0
  for i in range(total_length):
    v = abs(curr[i] - prev[i])
    if v > max_variance:
      max_variance = v

  return max_variance


def process_file(in_p, out_p=None):
  prev_value = []
  curr_value = []

  lines = in_p.readlines()
  idx = 0

  start = 4
  end = -8
  for line in lines:
    if not 'conv1' in line:
      continue
    else:
      idx += 1

    tmp = line.split('=')[1]
    tmp = tmp[start:end]
    tmp_value = tmp.split(' ')

    if idx % 2 == 0:
      curr_value = []
    else:
      prev_value = []
    for v in tmp_value:
      if idx % 2 == 0:
        curr_value.append(float(v))
      else:
        prev_value.append(float(v))
    if prev_value != [] and curr_value != []:
      variance = calculate_variance(prev_value, curr_value)
      if out_p:
        out_p.write(str(variance) + '\n')
      else:
        print("The max variance between %d and %d is %f" % (idx - 1, idx, variance))

  in_p.close()
  if out_p:
    out_p.close()

def main():
  if len(sys.argv) == 1:
    print("Error: need input file at least!")

  filename = sys.argv[1]
  out_p = None

  if len(sys.argv) == 3:
    out_file = sys.argv[2]
    out_p = open(out_file, 'a')

  in_p = open(filename)
  process_file(in_p, out_p)
  

if __name__ == '__main__':
  main()
