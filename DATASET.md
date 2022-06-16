# Data Set Description

This documents describes in details the dataset dataC used in the paper. This dataset is from JD, one of China's biggest e-commerce companies, with billions of customers and humongous amount of real commercial data. This dataset is provided as part of a competition where the contestants are required to build a machine learning model to predict the purchase intention of customers. The dataset is extracted from real customers from the JD mall, including product and user action log information. The intention is to predict customer's intention to purchase certain products, to match customers with products they desire.

* Data includes daily users from 2016-02-01 to 2016-04-15 (group U), behaviour, comments and user action information towards products in group S, and potential product information in group P.
* Acronyms definition:
	* S: all products;
	* P: potential products, P is a subset of S;
	* U: all users;
	* A: users action towards products in S;
	* C: comment information of products in S.
 
* Data Tables: 

 1. User Data

| Name <img width=100/> | Meaning <img width=160/>| Notes <img width=200/>|
|-------------|-----------------------|-----------------------------------------|
| user_id     | user ID               | Encoded                                 |
| age         | age group             | -1 for unknown                          |
| sex         | gender                | 0 for male, 1 for female, 2 for others  |
| user_lv_cd  | user level            | higher level bigger number              |
| user_reg_tm | user registration date | in days                                 |

2. Product Data

| Name <img width=100/> | Meaning <img width=160/>| Notes <img width=200/>|
|-------------|-----------------------|-----------------------------------------|
| sku_id      | product ID            | Encoded                                 |
| a1          | property 1            | -1 for unknown                          |
| a2          | property 2            | -1 for unknown                          |
| a3          | property 3            | -1 for unknown                          |
| cate        | category ID           | Encoded                                 |
| brand       | brand ID              | Encoded                                 |

3. Comments Data

| Name <img width=100/> | Meaning <img width=160/>| Notes <img width=200/>|
|-------------|-----------------------|-----------------------------------------|
| dt         | time until             | in days                                 |
| sku_id      | product ID            | Encoded                                 |
| comment_num | total number of comments  | 0 for no comments; 1 for 1 comment; <br> 2 for 2-10 comments; 3 for 11-50 comments; <br> 4 for above 50 comments.                        |
| has_bad_comment  | if product has bad comments | 0 for no; 1 for yes.         |
| bad_comment_rate | rate of bad comments        | ratio of bad comments in all comments|

4. Action Data

| Name <img width=100/> | Meaning <img width=160/>| Notes <img width=200/>|
|-------------|-----------------------|-----------------------------------------|
| user_id     | user ID               | Encoded                                 |
| sku_id      | product ID            | Encoded                                 |
| time        | time of action    |
| type        | type of action        | 1: browse; 2: put to cart; <br>3: remove from cart; 4: place order; <br>5: follow; 6: click |
| cate        | category ID           | Encoded                                 |
| brand       | brand ID              | Encoded                                 |

For more information, visit [[1]](#1) 


## Local Feature Extraction

We adopt our in-house feature engineering tools [[2]](#2)[[3]](#3) on the production AutoML platform HyperCycleML [[4]](#4) to perform feature extraction. The configuration of the original dataset is described in [config.json](dataset/config.json). The detailed operations on the featues are summarized in [feql.script](dataset/feql.script). The operations are described in Feature Enginnering QL (FEQL), an in-house feature descitptive language.

The extracted features by the aforementioned feature engineering tools are logically divided into three sets, from the sub-tables the features are generated:

- Static features: original features and non-time-related extracted features.
- Time series group A: time series features generated with time windows constructed for Action Data.
- Time series group B: time series features generated with time windows constructed for user product interaction logs.
- TIme series group C: time series features generated with time windows constructed for Comments Data. 

| Group               | Feature Names                                                |
| ------------------- | ------------------------------------------------------------ |
| Static features     | f_flattenRequest_bo_product_a1_direct_7, f_flattenRequest_bo_product_a2_direct_8, f_flattenRequest_bo_product_a3_direct_9, f_flattenRequest_bo_product_br_direct_10, f_flattenRequest_bo_product_cate_direct_11, f_flattenRequest_bo_user_age_direct_13, f_flattenRequest_bo_user_sex_direct_15, f_flattenRequest_bo_user_user_lv_cd_direct_16, f_original_pair_id_2, f_original_sku_id_3, f_combine_34_27, f_combine_35_29, f_combine_36_31, f_combine_37_34 |
| Time series group A | f_flattenRequest_bo_action_br_top3frequency_18, f_flattenRequest_bo_action_cate_top3frequency_19, f_flattenRequest_bo_action_model_id_top3frequency_20, f_flattenRequest_bo_action_type_top3frequency_21, f_flattenRequest_bo_action_model_id_distinct_count_24, f_flattenRequest_bo_action_model_id_distinct_count_25, f_flattenRequest_bo_action_type_distinct_count_26 |
| Time series group B | f_flattenRequest_window_unique_count_pair_id_30, f_flattenRequest_window_top1_ratio_pair_id_31, f_flattenRequest_window_top1_ratio_pair_id_32, f_flattenRequest_window_unique_count_pair_id_33, f_flattenRequest_window_count_pair_id_43, f_flattenRequest_window_count_pair_id_44 |
| Time series group C | f_flattenRequest_bo_comment_bad_comment_rate_avg_5, f_flattenRequest_bo_comment_bad_comment_rate_avg_6, f_flattenRequest_bo_comment_bad_comment_rate_min_17, f_flattenRequest_bo_comment_comment_num_distinct_count_27, f_flattenRequest_bo_comment_comment_num_distinct_count_28, f_flattenRequest_bo_comment_has_bad_comment_distinct_count_29 |

## Note

In federated time series feature extraction experiements, we assign Comments Data table to the collaborator. Thus time series group A and B are pregenerated in the Initiator, and time series group C is expected to be generated by the FTSFE process.

* Example data preparation for FTSFE

| Party               | Features       | Feature Details                                                |
| ------------------- | -------------- | ------------------------------------------------------------ |
| Initiator           | ids, static features, time series group A, time series group B |user_id, sku_id, f_flattenRequest_bo_product_a1_direct_7, f_flattenRequest_bo_product_a2_direct_8, f_flattenRequest_bo_product_a3_direct_9, f_flattenRequest_bo_product_br_direct_10, f_flattenRequest_bo_product_cate_direct_11, f_flattenRequest_bo_user_age_direct_13, f_flattenRequest_bo_user_sex_direct_15, f_flattenRequest_bo_user_user_lv_cd_direct_16, f_original_pair_id_2, f_original_sku_id_3, f_combine_34_27, f_combine_35_29, f_combine_36_31, f_combine_37_34, f_flattenRequest_bo_action_br_top3frequency_18, f_flattenRequest_bo_action_cate_top3frequency_19, f_flattenRequest_bo_action_model_id_top3frequency_20, f_flattenRequest_bo_action_type_top3frequency_21, f_flattenRequest_bo_action_model_id_distinct_count_24, f_flattenRequest_bo_action_model_id_distinct_count_25, f_flattenRequest_bo_action_type_distinct_count_26, f_flattenRequest_window_unique_count_pair_id_30, f_flattenRequest_window_top1_ratio_pair_id_31, f_flattenRequest_window_top1_ratio_pair_id_32, f_flattenRequest_window_unique_count_pair_id_33, f_flattenRequest_window_count_pair_id_43, f_flattenRequest_window_count_pair_id_44 |
| Collaborator        | ids, native comments data | sku_id, dt, comment_num, has_bad_comment, bad_comment_rate |
## References

<a id="1">[1]</a> JD Data Set. https://jdata.jd.com/html/detail.html?id=1.

<a id="2">[2]</a> OpenMLDB. 2021. An Open Source Database for Machine Learning Systems.https://github.com/4paradigm/OpenMLDB.

<a id="3">[3]</a> Chen, C.; Yang, J.; Lu, M.; Wang, T.; Zheng, Z.; Chen, Y.;Dai, W.; He, B.; Wong, W.-F.; Wu, G.; Zhao, Y.; and Rudoff,A. 2021. Optimizing In-Memory Database Engine for AI-Powered on-Line Decision Augmentation Using PersistentMemory.Proc. VLDB Endow., 14(5): 799–812.

<a id="4">[4]</a> HyperCycleML. 2021. An Automated Machine Learning Platform. https://en.4paradigm.com/product/hypercycleml.html


