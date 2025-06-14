# Project Valk

Our team made a 2D plaftformer video game with 10 unique levels in which the player's character tries to reach her sword.
Each level presents different challenges and get progressively harder. Only a few have succesfully completed the game. So the quesntion is... Are you up to the challenge?!




## Setup

Link to the gitlab: https://git.liacs.nl/m.kalnare/group-19-2d-platformer-ai.git

Important! - The game is tested on Python 3.9 and 3.10


setup for windows:
```
git clone git@git.liacs.nl:m.kalnare/group-19-2d-platformer-ai.git  #if SSH is set up. You can skip this step if you already have the project downloaded 
cd group-19-2d-platformer-ai            #open the project directory
py -m venv .venv                        #create venv 
.venv\Scripts\activate                  #activate venv
(venv) pip install -r requirements.txt         #install the req
(venv) cd src                                  #go to src
(venv) py main.py                          #run main


```

setup for linux (not tested):

```
$ git clone git@git.liacs.nl:m.kalnare/group-19-2d-platformer-ai.git
$ cd group-19-2d-platformer-ai  
$ python3 -m venv .venv
$ source .venv/bin/activate
(venv) $ pip install -r requirements.txt
(venv) $ cd src
(venv) $ python3 main.py        


```
In case something goes wrong during the setup process, you can find more information at https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments/ 

To run the tests, repeat all the steps above, however instead of main.py run either of tests_player.py, tests_tiles.py or tests_level_load.py:


```
python tests_player.py
#or
python tests_tiles.py
#or
python tests_level_load.py
```

## Contributors

Code and Game Mechanics Design - Ivan Bichev(aka watchthedoge), Matiss Kalnare <br>
Character and Enviroment Sprites Design - Teodor Ionescu  <br>
Level Design - Cristian Danailov <br>
Code Description - Matei Angeleanu <br>
Report and Presentation - Matei Angeleanu, Cristian Danailov, Raaed Khan <br>

## Demo and Screenshots 


Gameplay of level 1

![Gameplay of level 1](./Assets/gifs/AnimationValk1.gif)

Main menu

![](./Assets/gifs/Screenshot1.png)

Tutorial
![](./Assets/gifs/Screenshot2.png)

Level 9
![](./Assets/gifs/Screenshot3.png)

Example terminal for the setup of the game
```
Microsoft Windows [Version 10.0.22631.2861]
(c) Microsoft Corporation. All rights reserved.

C:\Windows\System32>pip list
Package    Version
---------- -------
pip        20.1.1
setuptools 47.1.0
WARNING: You are using pip version 20.1.1; however, version 23.3.2 is available.
You should consider upgrading via the 'c:\users\i_bic\appdata\local\programs\python\python38\python.exe -m pip install --upgrade pip' command.

C:\Windows\System32>cd..

C:\Windows>cd..\

C:\>cd \group-19-2d-platformer-ai

C:\group-19-2d-platformer-ai>py -m venv .venv

C:\group-19-2d-platformer-ai>.venv\Scripts\activate

(.venv) C:\group-19-2d-platformer-ai>pip install -r requirements.txt
Collecting contourpy==1.0.6
  Downloading contourpy-1.0.6-cp311-cp311-win_amd64.whl (163 kB)
     ---------------------------------------- 163.6/163.6 kB 9.6 MB/s eta 0:00:00
Collecting cycler==0.11.0
  Downloading cycler-0.11.0-py3-none-any.whl (6.4 kB)
Collecting fonttools==4.38.0
  Downloading fonttools-4.38.0-py3-none-any.whl (965 kB)
     ---------------------------------------- 965.4/965.4 kB 15.2 MB/s eta 0:00:00
Collecting kiwisolver==1.4.4
  Downloading kiwisolver-1.4.4-cp311-cp311-win_amd64.whl (55 kB)
     ---------------------------------------- 55.4/55.4 kB ? eta 0:00:00
Collecting matplotlib==3.6.2
  Downloading matplotlib-3.6.2-cp311-cp311-win_amd64.whl (7.2 MB)
     ---------------------------------------- 7.2/7.2 MB 8.2 MB/s eta 0:00:00
Collecting NuMPI==0.3.1
  Downloading NuMPI-0.3.1.tar.gz (48 kB)
     ---------------------------------------- 48.7/48.7 kB 2.6 MB/s eta 0:00:00
  Preparing metadata (setup.py) ... done
Collecting numpy==1.24.0
  Downloading numpy-1.24.0-cp311-cp311-win_amd64.whl (14.8 MB)
     ---------------------------------------- 14.8/14.8 MB 7.2 MB/s eta 0:00:00
Collecting packaging==22.0
  Using cached packaging-22.0-py3-none-any.whl (42 kB)
Collecting Pillow==9.3.0
  Downloading Pillow-9.3.0-cp311-cp311-win_amd64.whl (2.5 MB)
     ---------------------------------------- 2.5/2.5 MB 26.4 MB/s eta 0:00:00
Collecting pygame==2.5.2
  Downloading pygame-2.5.2-cp311-cp311-win_amd64.whl (10.8 MB)
     ---------------------------------------- 10.8/10.8 MB 24.2 MB/s eta 0:00:00
Collecting pyparsing==3.0.9
  Downloading pyparsing-3.0.9-py3-none-any.whl (98 kB)
     ---------------------------------------- 98.3/98.3 kB ? eta 0:00:00
Collecting python-dateutil==2.8.2
  Downloading python_dateutil-2.8.2-py2.py3-none-any.whl (247 kB)
     ---------------------------------------- 247.7/247.7 kB 14.8 MB/s eta 0:00:00
Collecting six==1.16.0
  Downloading six-1.16.0-py2.py3-none-any.whl (11 kB)
Installing collected packages: six, pyparsing, pygame, Pillow, packaging, numpy, kiwisolver, fonttools, cycler, python-dateutil, NuMPI, contourpy, matplotlib
  DEPRECATION: NuMPI is being installed using the legacy 'setup.py install' method, because it does not have a 'pyproject.toml' and the 'wheel' package is not installed. pip 23.1 will enforce this behaviour change. A possible replacement is to enable the '--use-pep517' option. Discussion can be found at https://github.com/pypa/pip/issues/8559
  Running setup.py install for NuMPI ... done
Successfully installed NuMPI-0.3.1 Pillow-9.3.0 contourpy-1.0.6 cycler-0.11.0 fonttools-4.38.0 kiwisolver-1.4.4 matplotlib-3.6.2 numpy-1.24.0 packaging-22.0 pygame-2.5.2 pyparsing-3.0.9 python-dateutil-2.8.2 six-1.16.0

[notice] A new release of pip available: 22.3 -> 23.3.2
[notice] To update, run: python.exe -m pip install --upgrade pip

(.venv) C:\group-19-2d-platformer-ai>cd src

(.venv) C:\group-19-2d-platformer-ai\src>py main.py
pygame 2.5.2 (SDL 2.28.3, Python 3.11.0)
Hello from the pygame community. https://www.pygame.org/contribute.html

(.venv) C:\group-19-2d-platformer-ai\src>py tests_playr.py
C:\Users\I_Bic\AppData\Local\Programs\Python\Python311\python.exe: can't open file 'C:\\group-19-2d-platformer-ai\\src\\tests_playr.py': [Errno 2] No such file or directory

(.venv) C:\group-19-2d-platformer-ai\src>py tests_player.py
pygame 2.5.2 (SDL 2.28.3, Python 3.11.0)
Hello from the pygame community. https://www.pygame.org/contribute.html
............
----------------------------------------------------------------------
Ran 12 tests in 0.428s

OK
```









Written by Ivan Bichev
