# **mma_2024**

Repository for the course in Multimedia Analytics at University of Amsterdam 2024


## **Setup**

### **Requirements**

To setup the environment, you can run the following script:

```sh

conda env create -f environment.yml

```

It can then be activated with:

```sh

conda activate mma_2024

```

Alternatively, you can use a virtual environment instead through the following commands:

```sh

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

```

### **Data**

The GTZAN dataset is currently only available on [Kaggle](https://www.kaggle.com/datasets/andradaolteanu/gtzan-dataset-music-genre-classification), meaning that an account is required to download it. Once downloaded, extract all the files in the `Data` folder to `dashboard/data/gtzan`. The dataset is ~1 GB large. 

Alternatively, we have prepared a script which automatically does this (though you still need to setup a Kaggle account and API to use this method):


```sh

python download_gtzan.py

```

In principle, any audio dataset can be used, as long as it is located in the `dashboard/data/[your_dataset_name]` folder and all files are in `.wav` (the sampling rate and lengths are automatically adjusted).

## **Running**

To run the code, you use the following:

```sh

python src/main.py

```

After the Dash server is running, open http://127.0.0.1:8050/ on your browser.
