import os
from calculate_variance import process_file

filepath="/vpublic01/frog/v-xuapen/benchmarks/scripts/tf_cnn_benchmarks/scripts/mem_log/"
out_filepath="/vpublic01/frog/v-xuapen/benchmarks/scripts/tf_cnn_benchmarks/scripts/result/"

def process_dir(path):
  files = os.listdir(path)
  for fi in files:
    fi_d = os.path.join(path, fi)
    if os.path.isdir(fi_d):
      process_dir(fi_d)
    else:
      in_filename=str(fi)
      in_fullname=filepath + in_filename
      out_filename=in_filename.split('.')[0] + ".txt"
      out_fullname=out_filepath + out_filename

      in_p=open(in_fullname)
      out_p=open(out_fullname, 'a')
      process_file(in_p, out_p=out_p)
      # print(os.path.join(path, fi_d))

if __name__ == '__main__':
  process_dir(filepath)
