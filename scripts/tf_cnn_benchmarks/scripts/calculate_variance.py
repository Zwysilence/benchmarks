total_length = 100
log_file = True

def calculate_variance(prev, curr):
  assert(len(prev) == total_length)
  assert(len(curr) == total_length)

  max_variance = 0
  for i in range(total_length):
    v = abs(curr[i] - prev[i])
    if v > max_variance:
      max_variance = v

  return max_variance



def process_file(in_p):
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
      if log_file:
        with open('out.txt', 'a') as out_p:
          out_p.write(str(variance) + '\n')
      else:
        print("The max variance between %d and %d is %f" % (idx - 1, idx, variance))

filename = 'tmp.log'
in_p = open(filename)
process_file(in_p)

in_p.close()
