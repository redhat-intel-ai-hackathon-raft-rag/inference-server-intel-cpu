read -p "Enter the path or name of the model you want to export: " model_path
optimum-cli export openvino \
    --model $model_path \
    --task 'text-generation' \
    --weight-format int4  \
    --group-size 128  \
    --dataset 'wikitext2' \
    --all-layers  \
    --scale-estimation  \
    --sensitivity-metric 'weight_quantization_error' \
    --cache_dir ./optimum_cache \
    ./openvino_exported_model