App setup:

    pyenv install 3.7.4
    mkvirtualenv wikisearch -p ~/.pyenv/versions/3.7.4/bin/python
    workon wikisearch
    pip install -r requirements.txt
    python -m nltk.downloader stopwords

To run the app:

    FLASK_ENV="development" FLASK_APP="app.py" flask run

To run the tests:

    FLASK_ENV="testing" nosetests tests
