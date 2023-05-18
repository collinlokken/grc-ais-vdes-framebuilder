# grc-ais-framebuilder
Python block AIS Framebuilder written for GNU Radio Companion >=3.8.

# Acknowledgments
This project was inspired by the works carried out by [Trendmicro](https://github.com/trendmicro/ais), who made the original AIS Frame Builder block in C++. Building on this, we have written an equivalent block in Python 3, which is now supported as an embedded block in GRC >=3.8. This block enables customization, and allows AIS ship values to be assigned at runtime using GRC widgets.

# Dependencies
Please also download and install the grc block for your SDR (Osmocom, UHD ...)

# Contents
AIS_Framebuilder.py		The python GRC frame builder block
AiS_TX.grc			GRC Flowgraph which can be imported into GNU Radio Companion
top_block.py			The full python program for the flow graph, runnable in the terminal
