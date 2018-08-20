import os
import sys
from calculate_variance import ProcessFile

filepath="/vpublic01/frog/v-xuapen/benchmarks/scripts/tf_cnn_benchmarks/scripts/"

def process_dir(path):
  if not os.path.exists(path):
    raise IOError

  files = os.listdir(path)
  for fi in files:
    fi_d = os.path.join(path, fi)
    if os.path.isdir(fi_d):
      continue
      # process_dir(fi_d)
    else:
      in_filename=str(fi)
      in_fullname=filepath + in_filename
      out_dir=out_filepath+in_filename.split('.')[0]+'/'
      if os.path.exists(out_dir):
        continue
      os.mkdir(out_dir)

      in_p=open(in_fullname)
      pf = ProcessFile()
      pf.process_max(in_p, out_dir=out_dir)
      # print(os.path.join(path, fi_d))

if __name__ == '__main__':
  rela_dir = ''
  if len(sys.argv) != 1:
    rela_dir = sys.argv[1]

  filepath += rela_dir
  out_filepath=filepath+'result/'
  if not os.path.exists(out_filepath):
    os.mkdir(out_filepath)
  process_dir(filepath)
