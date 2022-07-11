# Live Transcription With Python and Django

To run this project create a virtual environment by running the below commands. You can learn more about setting up a virtual environment in this article.

```
mkdir [% NAME_OF_YOUR_DIRECTORY %]
cd [% NAME_OF_YOUR_DIRECTORY %]
python3 -m venv venv
source venv/bin/activate
```

Make sure your virtual environment is activated and install the dependencies in the requirements.txt file inside.

`pip install -r requirements.txt`

Make sure you're in the directory with the manage.py file and run the project in the development server.

`python3 manage.py runserver`

Pull up a browser and go to your localhost, http://127.0.0.1:8000/.

Allow access to your microphone and start speaking. A transcript of your audio will appear in the browser.