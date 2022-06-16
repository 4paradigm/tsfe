cd data_upload
flow data upload -c dataA_upload_train_guest.json
flow data upload -c dataA_upload_train_host.json
cd ..

cd config
flow job submit -c dataA_training_conf.json -d training_dsl.json
