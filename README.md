# mod2mask
Creates binary mask from imod boundary model. 
Basically a re-implementation of ```sg_tm_create_boundary_mask.m``` from STOPGAP.

Call: ```mod2mask --boundary 20 1.rec 1.mod```

## Install

I recommend installing in a clean conda/mamba environment. 

```
conda create -n mod2mask python=3.9 -c conda-forge  
conda activate mod2mask  
pip install 'git+https://github.com/bwmr/mod2mask.git'
```
