import os
from calculate_variance import ProcessFile

filepath="/vpublic01/frog/v-xuapen/benchmarks/scripts/tf_cnn_benchmarks/scripts/mem_log/"
out_filepath=filepath+'result/'
os.mkdir(out_filepath)

def process_dir(path):
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
      os.mkdir(out_dir)

      in_p=open(in_fullname)
      pf = ProcessFile()
      pf.process_file(in_p, out_dir=out_dir)
      # print(os.path.join(path, fi_d))

if __name__ == '__main__':
  process_dir(filepath)
