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

We have created a custom version of the GTZAN dataset which already contains everything needed (i.e., the cover arts and metadata). This is downloaded automatically during startup.

Besides that, any audio dataset can be used, as long as it is located in the `dashboard/data/[your_dataset_name]` folder and all files are in `.wav` (the sampling rate and lengths are automatically adjusted).

To generate the metadata automatically, run the following:

```sh

python generate_metadata.py --data_loc [YOUR_FOLDER_HERE] # Folder containing the .wav files in `dashboard/data`

```

_Note:_ This process is quite slow and can take a long time depending on how large the dataset in question is. In addition, as this framework relies on Shazam, it is likely that some of the metadata fails to download if too many requests are made. We have tried to alleviate this, though, by adding a timer to delay the downloading when needed.


## **Running**

To run the code, you use the following:

```sh

python src/main.py

```

After the Dash server is running, open http://127.0.0.1:8050/ on your browser.
