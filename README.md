# Enercoodes


</p>
</details>

<br/>

<details> <summary> <b> Quickstart </b> </summary>
<p>

To copy this project, you need to clone the git repository on your computer.

**1. Set the virtual environment**

The python requirements are written in `./requirements.txt`

To create the virtual environment, follow the steps below:

Create the environment and activate it with the following commands:
```bash
PS C:\Users\...\enercoode> py -m venv .venv
PS C:\Users\...\enercoode> & .\.venv\Scripts\Activate.ps1
```

You can then install the required versions of the libraries by running
```bash
(.venv) PS C:\Users\...\enercoode> py -m pip install -r requirements.txt
```


**2. Set the solver path**

This program uses a non linear solver named ipopt (installation doc [here](https://coin-or.github.io/Ipopt/INSTALL.html))

Once installed, you need to set the value of `IPOPT_PATH` in `src/path.py` to point to the executable `ipopt.exe`

**3. Run the test**

Once the virtual environment is created and the paths are set, you can run the test script `test.py` or the illustrative notebook `Example.ipynb` 

</p>
</details>

<br/>

### Project structure

```bash
.
├── enercoode                           # Folder for project code and notebooks
│   ├── src                             # Folder for python scripts
|   |   ├── model.py                    # Module containing the functions to build the model
|   |   └── ...
│   ├── Example.ipynb                   # Illustrative notebook
│   └── test.py                         # script testing data folders.
├── .gitignore                          # File indicating which files/folder git must ignore (do not change/remove)
├── README.md                           # This file
└── requirements.txt                    # List the python libraries and versions to run the scripts.
```