# texfx: Extracting image files from LaTeX documents

texfx is a simple command-line program that extracts and renames figures
and their references in a LaTeX document. 

## Installation

````
git clone https://github.com/simonpf/texfx
cd texfx
pip install .
````

## Usage

````
texfx input_file.tex -o output_file.tex -d figure_directory
````
## Caveats

This package is still under development so it may not work as expected. Make
sure to check that the generated document contains all figures as expected.
