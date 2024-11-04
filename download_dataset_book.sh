file=dataset_book
tar_file=$file.tar.gz
jsonl_file=$file.jsonl
out_dir=dataset
PRESIGNED_URL_FOR_BUCKET=https://objectstorage.ap-osaka-1.oraclecloud.com/p/WKqZydY3o7G0jJ73v4E_VjJEhkzWO2XIuzA99VvwdKRi5jM1jAf6Ulgl22Vdxby9/n/axe0pnb37jb1/b/bucket-20241015-0858/o/$tar_file
curl -X GET -o $tar_file $PRESIGNED_URL_FOR_BUCKET
tar -xzf $tar_file && rm $tar_file
mkdir -p $out_dir
# cat $jsonl_file | jq -s '.' > $out_dir/$file.json
mv $jsonl_file $out_dir/$jsonl_file