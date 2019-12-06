# Instructions to run the code

## Directory Structure

```bash
.
│   README.md 
│   requirements.txt                                                                                                                  
│   DataAnalysis.py
│   main.py                                                                                                                             ├───Agent
│   └───BuildingAgent.py             <------ Agent Defined Here
├───Model 
│   └───BuildingModel.py             <------ Model Defined Here                                                                         ├───Data
│   │   buildings_data.csv
│   │   buildings_meta.json                                                                                                              │   └───Experiments
│       │   dual_extremism.json      <------ Macro Level Expt Params
│       │   uni_extremism.json       <------ Adjust scenarios
│       ├───dual_extremism
│       │       profile_0.json       <------ Profiles within the expt                                                                   │       │       profile_1.json
│       │       ...
│       └───uni_extremism
│               profile_0.json
│               profile_1.json
│               ...
├───Datalogs
│   └───Logs
│       └───uni_extremism
│               profile_0_Coordinates.csv
│               profile_0_HF.csv
│               profile_0_MF.csv
│               ...
├───Tools
│       DataloggingFunctions.py
│       RelativeAgreement.py
│       AnalysisFunctions.py
│       VisualizationFunctions.py
│       SimplePayback.py                                                                                                         └───Visualization
    └───res
        A_ext1_4_Run_30_Anim_IdeaEvolution.gif
        A_ext1_4_Run_30_Anim_PVEvolution.gif
        ...
```

## Installation

If you don't have **Python 3** installed and **added to PATH**, install it from [here]([https://www.python.org/downloads/release/python-375/](https://www.python.org/downloads/release/python-375/). 

> Note: Python 3.8 is not fully supported by some libraries. Not Recommended.

Also, install git if unavailable from [here]([https://git-scm.com/](https://git-scm.com/)

These instructions can be used with <u>bash</u> (Linux, MacOS) or <u>powershell</u> (Windows)

Clone the Repository from github:

```bash
git clone https://github.com/souryavarenya/Emergence-of-cooperation-Solar-communities.git
```

> One can also download the repository from [here](https://github.com/souryavarenya/Emergence-of-cooperation-Solar-communities/archive/master.zip)

Then enter the `code/` folder and install all the dependencies using the command below

```shell
cd Emergence-of-cooperation-Solar-communities/code/
pip install --user --requirement requirements.txt
```

> Note: These dependencies must be installed for python 3. Try `pip3` if your computer has multiple versions of python installed

Install ImageMagick from [here](https://imagemagick.org/script/download.php) (Needed for exporting GIF animations) 

## Running the code

### Running the experiment

An experiment can be launched by passing it's name as an argument while running the main script. The available experiments can be found in `/Data/Experiments/` folder as a JSON configuration file. You can also craft an experiment by cloning the existing ones and changing the parameters

```bash
python main.py uni_extremism
```

> Note: These scripts must be run with python 3. Try `python3` if your computer has multiple versions of python installed

Each experiment takes about 200-600s to complete based on the power of the machine it's running on. Grab a good cup of coffee while the pancake machine heats up!

Running these experiments will generate and save log files for visualization.

### Visualizing the Results

Once you have run an experiment, graphs can be generated as follows:

```
python DataAnalysis.py uni_extremism
```

That's it! You have successfully finished running an experiment and visualizing the data

---

## Miscellaneous

Below is an example of how experiment JSON (`Data/Experiments/<expt_name.json>`) looks like:

```json
{    
"experiment_name":"uni_extremism",    
"rel_profile_dir":"uni_extremism",    
"n_time_steps":150,    
"n_batches":50,    
"batch_seeds":[ 3662, 5290, 3650, 2610, 9334, 355, 374, 9327, 879,                        
                2781, 3947, 8253, 4539, 5269, 7042, 2345, 9222, 6581,                    
                3192, 2315, 7327, 283, 4494, 4418, 7219, 6015, 2973,                      
                9311, 5552, 4082, 6091, 6148, 9983, 5090, 6505, 5043,                     
                6878, 8951, 8451, 4135, 2754, 9849, 3721, 3777, 54,                     
                422, 2403, 2728, 7312, 132],    
"run_profiles":[0,1,2,3,4],    
"n_profiles":5,    
"show_plots": false,    
"save_plots": true,    
"batch_comparison": false,    
"single_batch": false,    
"batch_to_analyze": 1,    
"continuous_plots": false,    
"state_plots": false,    
"histogram_plots": false,    
"color_map_plots": false,    
"color_map_anims": false,    
"presentation_plots":true
}
```

> Note: For reproducibility, a list of seeds has been defined for each batch of an experiment in `Data/Experiments/<expt_name.json>` file. For running a fully randomized experiment, delete this key from the JSON file.

From this file, you can also configure what visualizations you'd want to see by setting them to true.  You can also choose to see or save the plots by changing the values of `show_plots` and `save_plots` keys.
