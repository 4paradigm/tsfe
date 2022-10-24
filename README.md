# Time Series Feature Extraction for Federated Learning
This repo details the implementation of time series features extraction in federated learning (TSFE). The implementation is based on two industry solutions: OpenMLDB [[1]](#1) and FATE [[2]](#2). OpenMLDB is an open-source full-stack solution by 4Paradigm to facilitate feature engineering in machine learning. It provides a set of practices to develop, deploy, and maintain feature engineering in production efficiently and reliably. Efficient time series feature extraction is one of the most important functionalities in OpenMLDB. FATE is a popular federated learning framework that provides common FL functionalities based on a federated learning protocol. However, OpenMLDB is not designed for federated learning, and FATE does not contain time series feature extraction. Based on this motivation, TSFE extends OpenMLDB's time series feature extraction functions based on the FATE's federated learning protocol, and is further integrated into FATE's FL pipeline.  

## How to run
Example configuration files and datasets are provided in [examples](examples), follow [RUN_GUIDE.md](examples/RUN_GUIDE.md) to run examples.

## Publication
This work has been published in the proceedings of the 31st ACM International Conference on Information & Knowledge Management, CIKM '22. Read [HERE](paper/3511808.3557176.pdf).

- Siqi Wang, Jiashu Li, Mian Lu, Zhao Zheng, Yuqiang Chen, and Bingsheng He. 2022. [A System for Time Series Feature Extraction in Federated Learning](https://dl.acm.org/doi/10.1145/3511808.3557176). In Proceedings of the 31st ACM International Conference on Information & Knowledge Management (CIKM) 2022.

## References
<a id="1">[1]</a> OpenMLDB. 2021. An Open Source Database for Machine Learning Systems. https://github.com/4paradigm/OpenMLDB.

<a id="2">[2]</a> FATE. 2019. FATE (Federated AI Technology Enabler). https://github.com/FederatedAI/FATE.
