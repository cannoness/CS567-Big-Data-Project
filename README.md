This is the readme.
Goals of this project:

Pull twitter data.
Try to analyze sentiment of 2016 election with tweets.

Instructions for using the script 'buildCodes.py' can be found here:

https://docs.google.com/document/d/1JvyUrBKupKM3wlrt7eFJTaifYNjtzMBD4E2mT55DJqg/edit

Using twythonInterface.py:

twythonInterface.py has been constructed to condense functionality in
Tweet Search into fewer modules, get rid of duplicate code, and make usage
easier by using python instead of individual main methods.


-start python.

-From the prompt>>> import twythonInterface as ti

-to search use

>>> ti.searchForTerms(<term>, <count>, <fileName>)

-to stream ids use:

>>> ti.steamIDsTo(<fileName>)

-Ctrl-C to interupt.  This is a messy quit.

-exit() to exit python