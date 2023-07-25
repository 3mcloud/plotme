# plotme

plot all the things in all the folders automatically but only if there have been changes

## Features
* save the plot's configuration/definition with the data (plot_info.json)
* pass-through to plotly
  * scatter plot
    * mode (markers or lines)
    * marker_symbols
    * constant lines
    * error bars
  * pio.template
* auto-detect data files (xls, xlsx, csv only)
* supported data files: xls, xlsx, csv, txt
* only re-generate plots if data or plot_info has changed, (-f to force re-generate)
* pre-process
* post-process (max, min, avg)
* specify data_root using argument or current directory
* finds plot_info files at any depth in the folder tree
* validation plot_info.json using jsonschema

### unimplemented ideas, in order of priority
0. sign exe and add to releases
1. create better tests
2. use folder/file name for default plot title
3. Hierarchical plot_info based on folder structure
4. yml support
5. pkl data file support
6. 3D plots
7. plot_info linter

## Install
* download exe from releases (windows only)
* install as module in a python environment: 
  * SSH: ```python -m pip install git+ssh://git@github.com/3mcloud/plotme.git```
  * HTTPS: ```python -m pip install https://github.com/3mcloud/plotme.git```

## How to use
* from command line: plotme(.exe) -h to see arguments
* from file explorer:
  1. move to data directory or above
  2. run once to generate a template of the plot_info.json
  3. modify the template as needed
  4. run again to generate plot(s)
* optional_text_plot_info.json (specification must end in plot_info.json)
  * [pio.templates](https://plotly.com/python/templates/)
  * [marker_symbols](https://plotly.com/python/marker-style/)

## Develop
1. clone 
1. Navigate into the folder or open the folder with your favorite python IDE
1. create conda env `conda create -n plotme python=3.8`
1. activate env `conda activate plotme`
1. install as -e package `python -m pip install -e .` - Note the dot at the end, it's important

## Build windows exe
1. follow Develop instructions
2. ```choco install visualstudio2019buildtools``` (needed to compile orderedset)
3. ```pip install nuitka orderedset zstandard```
4. ```python -m nuitka plotme --onefile --standalone --enable-plugin=numpy --enable-plugin=anti-bloat --include-package=plotly --include-package-data=plotly --mingw```

## Test
1. follow Develop instructions
2. Install packages to run automated tests `python -m pip install -e .[test]`
1. run tests