Educational Equity theme
========================

Installation
------------

Using this package in a buildout requires having nodejs and npm installed. Once
npm is installed, you can enable this theme in a universal installer buildout by
taking the following steps:

1) Copy the ``deploy.cfg`` and ``psu_addons.cfg`` files from this repository
   into the buildout root directory.
2) Run `bin/buildout -c deploy.cfg`
3) You should now see the theme respository in ``src/plonetheme.eeq``. Replace
   the cfg files you copied above with symlinks to the cfg files from the
   repository::

    $ ln -sf src/plonetheme.eeq/deploy.cfg src/plonetheme.eeq/psu_addons.cfg .

Updating the Code
-----------------

Running ``buildout`` will automatically update the theme code and compile the
theme resources. If changes were only made to the theme resources files, you can
clear the theme cache from the theming control panel, otherwise restart the
zeoclients to update the running code.


Credits
-------

Initial template:
    [StartBootstrap Business Frontpage](https://github.com/BlackrockDigital/startbootstrap-business-frontpage/)

Icons:
    Font Awesome (fortawesome.github.com/Font-Awesome)

Other:
    Bootstrap 4 (getbootstrap.com)
    html5shiv.js (@afarkas @jdalton @jon_neal @rem)
    jQuery (jquery.com)
