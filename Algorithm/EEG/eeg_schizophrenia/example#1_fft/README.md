
数据来源：https://repod.icm.edu.pl/dataset.xhtml?persistentId=doi:10.18150/repod.0107441

参考论文：Graph-based analysis of brain connectivity in schizophrenia
论文网址：https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0188629

数据集说明：
1) 正样本用户数：14
2) 负样本用户数: 14
3) 采样频率: 250hz
4) 追踪时间: 30 second

RESULTS.CSV 中给出了不同大小路径的结果

预处理文件：
首先输入并设置重要参数，例如采样频率、试验长度以及应用快速傅里叶变换（FFT）后选择的特征数量，带通滤波器范围。
模型文件：
在模型文件中直接运行代码，所有参数将自动设置。

重要提示：
不要忘记根据您的情况更改文件夹位置。


Data source: https://repod.icm.edu.pl/dataset.xhtml?persistentId=doi:10.18150/repod.0107441

Reference papers: Graph-based analysis of brain connectivity in schizophrenia
Paper URL:https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0188629

Dataset description:
1) Number of positive sample users: 14
2) Number of negative sample users: 14
3) Sampling frequency: 250hz
4) trail time: 30 Seconds

Results on different size of trails is given in RESULTS.CSV

Code description:
Preprocessing File:
1) First Enter and set the important Parameters, like sampling frequency, length of trail and number of features to selest after applying FFT, Band Pass Filter range 
Model File:
In model file just run the code as all the parameters will be automatically set 

Important:
Don't forgot to change the folder location according to yours


Preprocessing Files description:

1) data preprocessing : Simple preprocessing with no augmentation and upsampling
2) data_preprocessing_augmented_dataloader : Contain augmentation and also preprocessing
3) data_preprocessing_upsampling_manual : Contain manual upsampling and augementation


model files description:

1) model: 
no augmentation and upsampling method included

2) model_upsampling_manual : 
The data provided is already divided into batches using manual preprocessing method

3) model_upsampling_augmented_dataloader : 
The data is fed into pos and neg training file and then using pytorch Dataset Library, upsampling of minority class is done and also batches is created and made sure that there is no repetition in batches




File Sequence:

1) data preprocessing -------> model

2) data_preprocessing_upsampling_manual ------>model_upsampling_manual


3) data_preprocessing_augmented_dataloader -------->model_upsampling_augmented_dataloader






Upsampling of Minority Class and not mixing of same chunks in same batch using Dataset pytorch Library:


Upsampling of minority class:

In the CustomOversampledDataset class, the oversample_minority() method is called during initialization. This method calculates how many times the minority class needs to be repeated to match the size of the majority class. Then it repeats the minority class accordingly, combining it with the majority class. Additionally, if there is a remainder after the repeated minority class is added, a portion of the minority class is appended to the dataset to ensure that all minority samples are included. Therefore, this code effectively upsamples the minority class to balance the dataset.



Dividing minority into batches and ensuring no repeating values:

The NonRepeatingBatchSampler class serves the purpose of creating batches without repeating values. It inherits from BatchSampler, which samples indices sequentially. However, in the __iter__ method, instead of just sequentially sampling indices, it shuffles the indices using torch.randperm and then iterates over these shuffled indices. Within the iteration, it checks if the sample corresponding to the current index has been seen before. If it hasn't been seen before or if all samples have been seen, the index is added to the batch. This ensures that each batch contains unique samples. If the batch is filled or if it's the last batch and drop_last is set to False, the batch is yielded. Thus, this code effectively divides the dataset into batches without repeating values.




Upsampling of Minority Class and not mixing of same chunks in same batch using manual way:


Upsampling of minority class:
1) The code determines the number of batches based on either the maximum or minimum length of the positive and negative class training sets, depending on the train_set parameter. Then it divides both positive and negative class training sets into batches accordingly.

2) If the positive class training set is larger than the negative class training set, it initializes pos_batches_filled with deep copies of neg_batches, ensuring that there are enough batches for the larger class.

3) The code then iterates through the batches and checks if any batch is not filled up to the specified batch size. If a batch is not filled, it randomly selects samples from other filled batches and appends them to fill the batch.
This process effectively balances the class distribution by oversampling the minority class (whichever class is smaller) to match the size of the majority class.

Dividing minority into batches and ensuring no repeating values:


1) After ensuring that each batch is properly filled, the code proceeds to combine the batches of positive and negative samples, ensuring that each batch contains an equal number of samples from each class.

2) Within each combined batch, the code shuffles the samples to avoid any ordering bias.

3) Therefore, this code achieves the division of minority into batches and ensures that in each batch, there are no repeating values.