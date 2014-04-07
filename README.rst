PyPlaintext
============

A HTML to plaintext converter.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install pyplaintext

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/bitmazk/pyplaintext.git#egg=pyplaintext


Usage
-----

.. code-block:: python

    from pyplaintext import converter
    html = '<html><body>Hello world!</body></html>'
    parser = converter.HTML2PlainParser()
    result = parser.html_to_plain_text(html)


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 pyplaintext
    make develop
    make test
    open htmlcov/index.html

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch
