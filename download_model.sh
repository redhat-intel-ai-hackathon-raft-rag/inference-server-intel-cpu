model_file=finetuned_model.tar.gz

PRESIGNED_URL_FOR_BUCKET=https://objectstorage.ap-osaka-1.oraclecloud.com/p/oBZ7aGYm4ucCE2NhErN8Fh0PeoveMcl2hgUbrXl1IQp8_A4cKVCOArPIL2_OY6gI/n/axe0pnb37jb1/b/bucket-20241015-0858/o/$model_file
curl -X GET -o $model_file $PRESIGNED_URL_FOR_BUCKET &&
tar -xzf $model_file && rm $model_file
