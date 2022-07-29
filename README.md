# plotme

plot all the things in all the folders automatically but only if there have been changes

## Features
* scatter plot
  * points
  * lines
* auto-detect data files
* supported data files: xls, xlsx, csv
* only re-generate plots if data or plot_info has changed
* pre-process
* post-process
* specify data_root using argument or current directory

### unimplimented ideas, in order of priority
1. create executable
1. use folder names 
1. Hierarchical plot_info based on folder structure
1. yml support
1. plk data file support
1. generate template from cli
1. 3D plots

Templates configuration
-----------------------
    Default template: 'plotly'
    Available templates:
        ['ggplot2', 'seaborn', 'simple_white', 'plotly',
         'plotly_white', 'plotly_dark', 'presentation', 'xgridoff',
         'ygridoff', 'gridon', 'none']


## Develop
1. clone 
1. Navigate into the folder or open the folder with your favorite python IDE
1. create conda env `conda create -n plotme python=3.8`
1. activate env `conda activate plotme`
1. install as -e package `python -m pip install -e .` - Note the dot at the end, it's important

## Build exe
1. follow Develop instructions
1. ```pip install pyinstaller```
1. ```cd plotme```
1. ```pyinstaller plotme.py --onefile```

## Test
1. follow Develop instructions
2. Install packages to run automated tests `python -m pip install -e .[test]`
1. run tests