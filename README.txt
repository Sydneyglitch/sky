Title: SKY+

CREDITS
Code: Sdd
Art: Sdd
Audio: Sdd and freesound.org

------------------------------------------------------------------------------------

GAME

Building a tower. Blocks will appear from the side, and the player will need to press Space to stop them on top of the previous block. 
The unmatched part will be cut off, making it more difficult to place a block on top of the previous one. The goal is to build the tower as high as possible.

---------------------------------------------------------------------------------------

HOW TO RUN
Download the required libraries and files, then run the file named run_game.py.

---------------------------------------------------------------------------------------

LIBRARIES USED
pygame, button, gif_pygame, random, sys

'button', 'pygame' and 'gif_pygame' are needed to be installed by writing 'pip install package_name' into cmd 

--------------------------------------------------------------------------------------

TROUBLESHOOTING
 
 - pip install packaging

If you have a trouble installing 'button' package, you should:

 - Download 'button-0.03.post3' from pypi.org/project/button/

 - Unzip it

 - In setup.cfg, change 'description-file' to 'description_file'

 - In setup.py, change python_requires=">=3.*", to python_requires=">=3.7",

 - Clear the pip cache(type 'pip cache purge' in cmd) and 
 update setuptools and wheel('pip install --upgrade --force-reinstall setuptools wheel')

 - Write 'cd' and the path to setup.py file to cmd. After that, write 'pip install .'

--------------------------------------------------------------------------------------

LICENSE

This game is released under the MIT License.

--------------------------------------------------------------------------------------

This is a simple skyscraper-building game. My very first game ever, made for my first game jam ever. 
I’m really glad for the experience, thank you :]

