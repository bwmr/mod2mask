import click
import mrcfile
import imodmodel

import numpy as np

from pathlib import Path
from model2mask import utils


@click.command
@click.option('--boundary', default = 0, type = int, 
              help = 'Crop this many pixels in XY.')
@click.argument('tomogram', type = click.Path())
@click.argument('modfile', type = click.Path())
def mod2mask(boundary, tomogram, modfile):
    '''
    model2mask

    Basically, a Python implementation of sg_tm_create_boundary_mask.m from 
    STOPGAP.
    
    Takes as input a tomogram and the imod boundary model. Additionally, an xy 
    crop region can be defined.
    
    Outputs a binary mask named tomogram-name_mask.mrc.

    '''
    
    modfile = Path(modfile)
    tomogram = Path(tomogram)
    
    # Get dimensions
    with mrcfile.mmap(tomogram, mode='r') as mrc:
        dims = mrc.data.shape
        angpix = mrc.voxel_size
        
    # Get boundary model
    model = imodmodel.read(modfile)
    
    # Create output mask, with correct XYZ
    mask = np.zeros(shape = [dims[2],dims[1],dims[0]], dtype = np.int16)
    
    # Sort model into top and bottom
    top, bottom = utils.parse_top_bottom(model)
    
    # Fit planes
    [atop, btop, ctop] = utils.fit_plane(top)
    [abot, bbot, cbot] = utils.fit_plane(bottom)

    # Sanity check: how thick is the volume, what angle are the planes
    
    print(f'Thickness of {modfile.name} is estimated {round(utils.distance(atop, btop, ctop, abot, bbot, cbot, dims[2], dims[1])* angpix.x / 10)} nm.')
    print(f'Top and bottom plane have an angle of {round(utils.angle(atop, btop, ctop, abot, bbot, cbot))} deg to each other. \n')
    
    # Very unelegant way to iterate over xy plane
    for i in range(0,dims[2]):
        for j in range(0, dims[1]):
            z1 = round(utils.plane(i+1, j+1, [atop, btop, ctop]))
            z2 = round(utils.plane(i+1, j+1, [abot, bbot, cbot]))
            
            mask[i,j, z2:z1] = 1
            
    # If boundary is given, apply
    if boundary != 0:
        mask[0:boundary,:,:] = 0
        mask[:,0:boundary,:] = 0

        mask[dims[2]-boundary:,:,:] = 0
        mask[:,dims[1]-boundary:,:] = 0
    
    # Transpose mask to ZYX order
    mask = np.swapaxes(mask, axis1=0, axis2=2)
    
    # Write mrc file
    with mrcfile.open(tomogram.with_name(f'{tomogram.stem}_mask.mrc'), mode = 'w+') as mrc:
        mrc.set_data(mask)
        mrc.set_voxel_size = str(angpix)
        mrc.update_header_stats()
