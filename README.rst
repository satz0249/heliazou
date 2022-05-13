.. figure:: https://zou.cg-wire.com/zou.png
   :alt: Zou Logo

Zou is the memory of your animation production
----------------------------------------------

Zou is an API that stores and manages data related to animation productions. It allows you to centralize 
and access to all your data. Your tools connect to it and query the data from your production. Your 
Artists manage their files and their tasks more efficiently. It helps them to spend more time on the 
artistic side. 

A dedicated Python client, `Gazu <https://gazu.cg-wire.com>`_, allows users to integrate Zou into the tools. 

|Build badge| |Downloads badge|

Features
~~~~~~~~

Zou can:

-  Store production data, such as projects, shots, assets, tasks, metadata files,
   and validations.
-  Track the progress of your artists
-  Store preview files and version them
-  Provide folder and file paths for any task.
-  Import and Export data to CSV files.
-  Provide helpers to manage workflow tasks (start, publish, retake).
-  Listen to events to plug external modules on it.

Installation and documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Installation of Zou requires the setup of third-party tools such as a database instance, so it is recommended
to the follow the documentation:

`https://zou.cg-wire.com/ <https://zou.cg-wire.com>`__

Contributing
------------

Contributions are welcomed so long as the `C4
contract <https://rfc.zeromq.org/spec:42/C4>`__ is respected.

Zou is based on Python and the `Flask <http://flask.pocoo.org/>`__
framework.

You can use the pre-commit hook for Black (a python code formatter) before commiting :

.. code:: bash

    pip install pre-commit
    pre-commit install

Instructions for setting up a development environment are available in
`the documentation <https://zou.cg-wire.com/development/>`__


Contributors
------------

* @aboellinger
* @BigRoy (Colorbleed)
* @flablog (Les Fées Spéciales)
* @frankrousseau (CGWire) - *maintainer*
* @g-Lul (TNZPV)
* @pcharmoille (Unit Image)

About authors
~~~~~~~~~~~~~

Zou is written by CGWire, a company based in France. We help teams of animation
studios to collaborate better. We provide tools to more than 50 studios spread
all around the world.

On the technical side, we apply software craftmanship principles as much as
possible. We love coding and consider that strong quality and good developer
experience matter a lot.

Visit `cg-wire.com <https://cg-wire.com>`__ for more information.

|CGWire Logo|

.. |Build badge| image:: https://app.travis-ci.com/cgwire/zou.svg?branch=master
   :target: https://app.travis-ci.com/cgwire/zou
.. |Gitter badge| image:: https://badges.gitter.im/cgwire/Lobby.png
   :target: https://gitter.im/cgwire/Lobby
.. |CGWire Logo| image:: https://zou.cg-wire.com/cgwire.png
   :target: https://cgwire.com
.. |Downloads badge| image:: https://static.pepy.tech/personalized-badge/zou?period=total&units=international_system&left_color=grey&right_color=orange&left_text=Downloads
   :target: https://pepy.tech/project/zou
