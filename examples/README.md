# Examples Folder - Test Features Locally

The example projects are meant to be used to test features locally by contributors working on this SDK. In the `requirements.txt` file, the deepgram package used is the local version:

```
-e ../../
```

## Steps to Test Your Code

If you are contributing changes to this SDK, you can test those changes by using the `prerecorded` or `streaming` projects in the `examples` folder. Here are the steps to follow:

### Add Your Code
Make your changes to the SDK (be sure you are on a branch you have created to do this work).

### Install dependencies

Run the following command to install the project dependencies:

`pip install -r requirements.txt`

### Edit the API key

Replace the API key where it says 'YOUR_DEEPGRAM_API_KEY'

`DEEPGRAM_API_KEY = 'YOUR_DEEPGRAM_API_KEY'`

### Run the project

Make sure you're in the directory with the `main.py` file and run the project with the following command.

`python3 main.py`

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
