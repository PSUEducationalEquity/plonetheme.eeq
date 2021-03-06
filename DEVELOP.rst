Using the development buildout
==============================

After checkout you need to initialize and update the git submodule (for
barceloneta):

    $ git submodule init; git submodule update

Create a virtualenv in the package::

    $ virtualenv --clear .

Install requirements with pip::

    $ ./bin/pip install -r requirements.txt

Run buildout::

    $ ./bin/buildout

Start Plone in foreground:

    $ ./bin/instance fg

Theme development
-----------------

You need to have npm installed to compile the theme files. It's probably best to
match the deployed versions of nodejs v10.19.0 and npm v6.14.4.

Run `npm install` in the package root to setup scripts and dependencies::

    $ npm install

If there are any npm resources needed for the theme compilation defined in the
theme package.json, run the following to install/update them::

    $ cd ./src/plonetheme/eeq/theme
    $ npm install

After executing these commands you can run grunt on the package root folder to
watch for any less changes::

    $ npm run watch

This will make sure that the many .less files are compiled to .css on the fly
and then served up from the theme.

You can also use this command to automaticly reload the browser after changes::

    $ npm run plone-bsync

It will run a Grunt browser sync task in a new browser window and will reload
after every change of the less files in the less folder. If your Plone is not
running on port 8080 you have to adjust the proxy option in the Gruntfile.js.

You can also view the base theme file in a browser with automatic CSS change
syncing using::

    $ npm run bsync

If you prefer to do a one time compile of the less files you can run::

    $ npm run compile

The buildout will automatically install npm packages and run the compile.


Bootstrap Override
------------------

This theme incorporates Bootstrap v4 and Plone 5.2 includes portions of
Bootstrap v3 javascript in it's primary ``plone`` resources bundle. To avoid
conflicting implementation, the theme includes a customized compile of the
``plone-compiled.min.js`` resource that removes it. That custom bundle can
be updated using a script::

    $ cd bundle_update
    $ ./update_plone_resources.sh

This step should only be necessary after upgrading Plone itself, and only if the
``plone.staticresources`` version was changed. The current build is based on
version ``1.4.2`` of ``plone.staticresources``. After updating these resources,
you will probably need to reinstall the
``plone.staticresources EXPERIMENTAL: Async Resource Loading`` product from
``portal_quickinstaller`` to rebuild the bundle.

You need to have a site installed at ``/equity`` with the theme already installed
and updated to successfully run this command.


Theme Structure
---------------

The theme CSS is compiled (by npm/grunt) from LESS files ein the ``theme/less``
directory. The ``theme.less`` file imports modules and mixins from
``plonetheme.barceloneta`` (pulled in as a git submodule) along with theme
specific styles.

Basic theme variable config changes can be made in ``theme.vars.less`` which
contains less variables from plone that can be used to override default values.
Similarly ``plone.toolbar.vars.less`` contains variables specific to styling the
plone toolbar.


Note
----
- If you want to add other resources to your theme, add them to the
  bootstrap example in the package.json of the theme folder and run npm install
  there.


Buildout Configuration
----------------------

Custom buildout configuration should be added to ``psu_addons.cfg``, and
production specific config should be added to ``deploy.cfg``.


Running tests
-------------

    $ tox

list all tox environments:

    $ tox -l
    py27-Plone43
    py27-Plone51
    py27-Plone52
    py37-Plone52
    build_instance
    code-analysis
    lint-py28
    lint-py38
    coverage-report

run a specific tox env:

    $ tox -e py38-Plone52
