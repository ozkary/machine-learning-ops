# Prepare your data

- After you've collected the data, you need to create a data asset in Azure Machine Learning. In order for AutoML to understand how to read the data, you need to create a MLTable data asset that includes the schema of the data.

```
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml import Input

my_training_data_input = Input(type=AssetTypes.MLTABLE, path="azureml:input-data-automl:1")

```

## Configure AutoML Experiment

```
from azure.ai.ml import automl

# configure the classification job
classification_job = automl.classification(
    compute="aml-cluster",
    experiment_name="auto-ml-class-dev",
    training_data=my_training_data_input,
    target_column_name="Diabetic",
    primary_metric="accuracy",
    n_cross_validations=5,
    enable_model_explainability=True
)

```

- AutoML needs a MLTable data asset as input. In the example, my_training_data_input refers to a MLTable data asset created in the Azure Machine Learning workspace.