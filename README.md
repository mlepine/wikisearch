# WikiSearch

Randomly pulls documents from Wikipedia, indexes them and provides an REST api for searching.

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

Endpoints:

[/api/search?q={search}](http://localhost:5000/api/search?q=startups)
Lists documents matching the search query (q) and with a relevancy score.

[/api/docs](http://localhost:5000/api/docs)
Lists all documents.

[/apo/docs/{id}](http://localhost:5000/api/docs/1)
Returns a document with the given id.

[Demo App](http://localhost:5000/)
An demo app for testing the search.
