# Ukraine Support Gravity Plot

This repository contains Python code to analyze and visualize the gravitational center of European Union (EU) assistance to Ukraine. The script aggregates EU assistance data by country and uses the KMeans clustering algorithm to determine the optimal point representing the center of gravity of the assistance. The results are visualized on a map using Matplotlib and Basemap.
Installation
Conda Environment

    Clone this repository:

    bash

git clone https://github.com/your-username/ukraine-support-gravity.git

Navigate to the project directory:

bash

cd ukraine-support-gravity

Set up the Conda environment using the provided environment.yml file:

bash

conda env create -f UkraineGravity.yml

Activate the Conda environment:

bash

    conda activate ukraine-support-gravity

Virtual Environment (venv)

    Clone this repository:

    bash

git clone https://github.com/your-username/ukraine-support-gravity.git

Navigate to the project directory:

bash

cd ukraine-support-gravity

Create a virtual environment (optional but recommended):

bash

python3 -m venv env

Activate the virtual environment:

    Linux/macOS:

    bash

source env/bin/activate

Windows:

bash

    .\env\Scripts\activate

Install the required packages using requirements.txt:

bash

    pip install -r requirements.txt

Usage

To run the analysis and visualization, execute the run.py script:

bash

python run.py

This script will extract relevant data from an Excel file (ukrainesupporttracker.xlsx), perform clustering using KMeans with weights based on the percentage of 2021 GDP, and plot the results on a map.

Big thanks go to ChatGPT, which also wrote this readme!