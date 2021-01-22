# experience-oim-under-dcm
### experiment environment

python 3

### dataset

- put raw file `flickrEdges.txt` and `netHEPTEdges.txt` under direction `\DataProcess\raw\`
- run `DataProcess/SampleSmallGraph.py` , `SampleSubGraph.py` to generate network
- run files under  direction `SampleFeature` to generate related features

### main

under the root directory, run

```python
python3 Syn.py
```

the results will be saved under `\SimulationResults\[dataset]\[alg]`, which can be declared in `Syn.py`

the same for `Fixed.py` and `Interval.py`

### draw results

under the `visualizationTools`,  run 

````python
python drawResults.py
````

you can specify:

- `fileFolderPath`: where the results you want to draw stored
- `alg_list`: the baseline algorithms you want to draw,  in the form: `([dir_name], [colum_tag], [coclor], [label])`
- `count`: the rounds you want to draw
- `issave`: save the file or not
- `file_name`: the name of your stored file
- `subTitle`: the title of your picture

### file structure

 ``` python
. 
| BanditAlg # Baselines for running influence maximization problems.
| DataProcess
    ├── raw # store raw file describe the graph
    ├── SampleSmallGraph.py # sample syn graph
    ├── SampleSubGraph.py # sample sub graph from large dataset Flickr/NetHEPT
| datasets # store each dataset's graph and useful feature
| Model
    ├── IC.py, DC.py # run on IC/DC model to get reward
| Oracle
    ├── CMAB.py, Greedy.py, Greedy_IC.py # offline oracle for CMAB, DC and IC
| RunTools # function to run on different baseline
| SampleFeature
    ├── FeatureVector.py # 
    ├── Indegree.py # count the indegree of every node in graph
    ├── NodeFeature.py # generate
    ├── Probability.py # generate interval or fixed probablity
| SimulationResults # store the results of experiment
| Tool # helpful tools
| visualizationTools # draw the result, count the average
| Syn.py, Fixed.py, Interval.py # call RunTools to run choosen baseline
 ```