

## Azure CLI and ML Extenion

The Azure CLI is designed for automating tasks. By using YAML files to define how the model must be trained, the machine learning tasks will be repeatable, consistent, and reliable.

### install the CLI
```
$ sudo apt install azure-cli
$ az extension add -n ml -y
```

### Create a resource group and a workspace

```
$ az group create --name "rg-dp100-labs" --location "eastus"

$ az ml workspace create --name "mlw-dp100-labs" -g "rg-dp100-labs"
```

### Create a VM instance

```
 $ az ml compute create --name "aml-cluster" --size STANDARD_DS11_V2 --max-instances 2 --type AmlCompute -w mlw-dp100-labs -g rg-dp100-labs
```

## Python Scripts

### Install the python dependencies

Python 3.7 is required

```
$ pip install azure-ai-ml
```

### 

```
 git clone https://github.com/MicrosoftLearning/mslearn-azure-ml.git azure-ml-labs

```
   Open the Labs/02/Run training script.ipynb notebook.

### Write a script to connect to the workspace and authenticate

```

from azure.ai.ml import MLClient
from azure.identity import DefaultAzureCredential
from azure.ai.ml import command

ml_client = MLClient(
    DefaultAzureCredential(), subscription_id, resource_group, workspace
)

# configure job
job = command(
    code="./src",
    command="python train.py",
    environment="AzureML-sklearn-0.24-ubuntu18.04-py37-cpu@latest",
    compute="aml-cluster",
    experiment_name="train-model"
)

# connect to workspace and submit job
returned_job = ml_client.create_or_update(job)


```

###  Make the data available

- Install the MLTable library

```
 $ pip install mltable
```

- Create a datastore and data asset

