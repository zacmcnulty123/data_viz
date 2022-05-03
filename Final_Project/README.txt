The modules required to be installed to run the visualize script are
itertools, os, sys, numpy, pandas, and plotly.graph_objects

RUNNING THE VISUALIZE SCRIPT

This script is written in python3

There were 206 total rallies completed. Some rallies cannot be visualized because
there was missing data. If a rallyId that cannot be visualized is chosen the 
script will throw an error. This script assumes the the Tennis Data directory is colocated with
the script. 

running the script via cmdline:

python visualize.py <rallyid>

Example: python visualize.py 63 or python3 visualize.py 63

What will happen is a new tab will be opened on your default web browser
and you can play your visualization with the play button

The EDA Notebook can be launched in a Jupyter Notebook
The EDA notebook if you'd like to rerun the cells requires
os, pandas, plotly, cufflinks, matplotlib, and numpy

