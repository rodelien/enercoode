# Enercoode

<br/>

<details><summary> <b> Project Overview </b> </summary>
<p>



</p>
</details>

<br/>

<details> <summary> <b> Quickstart </b> </summary>
<p>

To copy this project, you need to clone the git repository on your computer.

The python requirements are written in `./requirements.txt`

**Locally**

To create the virtual environment, follow the steps below:

**0.** Start by checking that you are not currently in a virtual environment, to do so, you can run the command below:
```bash
PS C:\Users\...\enercoode> py -m pip -V
pip *.*.* from C:\Users\...\AppData\Local\Programs\Python\Python3*\lib\site-packages\pip (python 3.*)
```
which should indicate the python distribution installed locally (to exit from a venv, just run the command `deactivate`)

**1.** Create the environment and activate it with the following commands:
```bash
PS C:\Users\...\enercoode> py -m venv .venv
PS C:\Users\...\enercoode> & .\.venv\Scripts\Activate.ps1
```

**2.** You can then install the required versions of the libraries by running
```bash
(.venv) PS C:\Users\...\enercoode> py -m pip install -r requirements.txt
```
</p>
</details>

<br/>

### Project structure

```bash
.
├── enercoode                           # Folder for project code and notebooks
│   ├── src                             # Folder for python scripts
|   |   ├── path.py                     # Module containing project path variables
|   |   └── ...
│   └── main.py                         # script testing data folders.
├── .gitignore                          # File indicating which files/folder git must ignore (do not change/remove)
├── README.md                           # This file
└── requirements.txt                    # List the python libraries and versions to run the scripts.
```