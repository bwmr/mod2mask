from setuptools import setup

setup(
    name="model2mask",
    version="0.1",
    packages=['model2mask'],
    install_requires=[
        'imodmodel',
        'mrcfile',
        'scipy',
        'Click'
    ],
    entry_points={
	'console_scripts': [
        	'mod2mask = model2mask.mod2mask:mod2mask',
        ],
    },
    python_requires=">=3.9",
    author="bwmr",
    description="Create binary mask based on imod boundarymask.",
    url="https://github.com/bwmr/mod2mask"
)
