# gumimaci
A simple tool for my Python projects, so I can automatically test, build and create a release.
The following is used:
- nosetests:  For testing
- cx_freeze:  For creating windows executables

Tests are to be put in a "tests" directory.
The name of the .exe will be the the repo name + current date/time.

This won't be useful for any other programming language.

Simply put a "gumimaci" file in the root for your repository, and let the script run.
