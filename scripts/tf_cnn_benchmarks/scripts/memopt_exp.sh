log_dir="/vpublic01/frog/v-xuapen/benchmarks/scripts/tf_cnn_benchmarks/scripts/"

models="inception3"
# models="vgg16 inception3 resnet50 resnet152"
batch_sizes="64 128"
memory_optimizers="NO_MEM_OPT"
# memory_optimizers="NO_MEM_OPT SWAPPING_HEURISTICS RECOMPUTATION_HEURISTICS SCHEDULING_HEURISTICS HEURISTICS"
num_batches="50"
cuda_devices="0"

run(){
  ./localpsc.sh $1 $2 $3 $4 $5 $6 $7
}

for model in $models
do
  for batch_size in $batch_sizes
  do
    for memory_optimizer in $memory_optimizers
    do
      num_gpu=$(echo $cuda_devices | tr -d ',' | wc -l)
      log_name=$log_dir$model"_"$batch_size"_"$memory_optimizer".log"
      run $cuda_devices $num_gpu $batch_size $num_batches $model $memory_optimizer $log_name
    done
  done
done

