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

-from *nix systems, use included shell script tiStarter

Otherwise:

-from prompt: python -i tiStarter.py (This runs tiStarter.py which imports
twythonInterface as ti), then continues in interactive mode.

-call methods in twythonInterface in interactive mode with ti.methodName(args)

For example: ti.man() shows instructions.


-exit() to exit python.  All running threads should stop at this point.