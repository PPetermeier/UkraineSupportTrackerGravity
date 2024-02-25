# Ukraine Support Gravity Plot

This repository contains Python code to analyze and visualize the gravitational center of European Union (EU) assistance to Ukraine. The script aggregates EU assistance data by country and uses the KMeans clustering algorithm to determine the optimal point representing the center of gravity of the assistance. The results are visualized on a map using Matplotlib and Basemap.
## Installation
### Conda Environment
Clone this repository:

    git clone https://github.com/your-username/ukraine-support-gravity.git

Navigate to the project directory:


    cd ukraine-support-gravity

Set up the Conda environment using the provided environment.yml file:

    conda env create -f UkraineGravity.yml

Activate the Conda environment:


        conda activate ukraine-support-gravity

### Virtual Environment (venv)

Clone this repository:


    git clone https://github.com/your-username/ukraine-support-gravity.git

Navigate to the project directory:


    cd ukraine-support-gravity

Create a virtual environment (optional but recommended):


    python3 -m venv env

Activate the virtual environment:

Linux/macOS:

    source env/bin/activate
Windows:

    .\env\Scripts\activate

Install the required packages using requirements.txt
(If you use uv, it will be quite faster than normal pip:
https://astral.sh/blog/uv):
    pip install uv
    uv pip install -r requirements.txt

Usage

To run the analysis and visualization, choose which type of analysis you would like to run and call the specific function from main.py, e.g.:


    if __name__ == '__main__':
        run_concentricity()


    

This script will extract relevant data from an Excel file (ukrainesupporttracker.xlsx), perform clustering using KMeans with weights based on the percentage of 2021 GDP, and plot the results on a map.

Big thanks go to ChatGPT (https://chat.openai.com/), which also wrote this readme!
The team also got bitter, as I used https://www.perplexity.ai/ , which is really great as a gateway to the internet.


## Sources:

https://github.com/icyrockcom/country-capitals/blob/master/data/country-list.csv


https://www.ifw-kiel.de/topics/war-against-ukraine/ukraine-support-tracker/


## Changelog: 
- Added reference to uv in the *readme.md* concerning using pip. It is just way faster with nearly zero downside
- Adjusted naming conventions to better represent different modi of plotting
- Added *get_capital_name* and updated *extract_support_gravity_center* as well as the parquet-file with a new column "Capital" in order to make plotting easier
- Added *run_concentricity* and the resulting plot