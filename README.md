# plotme

plot all the things in all the folders automatically but only if there have been changes


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