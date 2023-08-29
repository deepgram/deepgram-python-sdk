# Examples for Testing Features Locally

The example projects are meant to be used to test features locally by contributors working on this SDK, but they can also be used as quickstarts to get up and running with the Deeegram Python SDK.

Here are the steps to follow to run the examples with the **local version** of the SDK:

## Add Your Code

Make your changes to the SDK (be sure you are on a branch you have created to do this work).

## Install dependencies

You can choose between two methods for installing the Deepgram SDK from the local folder:

### Install locally with the `examples/<example>/requirements.txt` file

Move to within the `examples/<example>` folder and run the following command to install the project dependencies. This command will install the dependencies from the local repo due to the package being added as `-e ../../` The`-e` indicates that a package should be installed in "editable" mode, which means in-place from the source code (local folder).

`pip install -r requirements.txt`

### Install locally with `pip install -e`

The other method that can be used to install the Deepgram SDK from the local project is to use `pip install -e`. In this case, you would:

```
pip uninstall deepgram-sdk # If it's already installed
cd /path/to/deepgram-python-sdk/ # navigate to inside the deepgram SDK
pip install -e .
```

This will install the SDK from the local source code in editable mode, so any changes made inside the project will be instantly usable from the example files.

### Edit the API key

Inside the example file, replace the API key where it says 'YOUR_DEEPGRAM_API_KEY'

`DEEPGRAM_API_KEY = 'YOUR_DEEPGRAM_API_KEY'`

### Run the project

Make sure you're in the directory with the `main.py` file and run the project with the following command.

`python main.py`

### After testing

After you have used the example files to test your code, be sure to reset the example file to the way it was when you started (i.e. discard features you may have added to the options dictionary when testing features).

## How to verify that you're testing the local changes

If you want to be sure that you are testing the local `deepgram` package, you can run this check.

### Step 1

Launch the Python interpreter by typing `python` in the terminal. Make sure you are in the folder with the `main.py` file you will be using to run the test.

```
python
```

### Step 2

Inside the interpreter, run the following code. This will import the `importlib` modules and use `find_spec()` to determine the location of the imported module.

```py
import importlib.util

spec = importlib.util.find_spec("deepgram")
if spec is not None:
    print("Module 'deepgram' is imported from:", spec.origin)
else:
    print("Module 'deepgram' is not found.")

```

This code checks whether the module named "deepgram" is imported and, if so, prints its origin (i.e., the location from where it's imported).
