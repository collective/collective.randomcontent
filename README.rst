.. contents::


Documentation
=============


What is this?
-------------

This package defines several browser views that do a redirect to
random content.


Use case
--------

The main use case would be: a random header background image.  Use
``@@randomimage`` as background image in a css file.  When the browser
loads the css file and wants to apply the background image, it will
get redirected to the image.

Example css code for when you want a random background image on all
pages except the front page, is this::

  #portal-header {
    background: url(@@randomimage) no-repeat 0 0;
  }
  .section-front-page #portal-header {
    background: #ee0;
  }


Alternative
-----------

`collective.randomheaderimage`_ achieves the same thing as using
``@@randomimage`` in a css file.  It does this by overriding the
``plone.header`` viewlet and adding some inline css to it.  This works
fine.  It has one possible drawback: if you use caching, then you
always get the same image for a page, until the cache gets refreshed.
This may or may not be a problem for you.

.. _`collective.randomheaderimage`: http://pypi.python.org/pypi/collective.randomheaderimage


Installation and configuration
------------------------------

Add ``collective.randomcontent`` to the eggs of your buildout (zcml is
not explicitly needed), rerun buildout and start your zope instance.

Install ``collective.randomcontent`` in the Site Setup.  Go to its
control panel and choose a folder in your site where we take images
from.

Note that when you only want to use ``@@randomsiteimage`` or
``@@randomsitecontent``, you do not need to install this package in
the site setup.


Details
-------

The following views are available:

- ``@@randomimage``: this picks a random image from your site and
  redirects to this url.  The image must be in a specific folder, that
  you set in the control panel.

- ``@@randomsiteimage``: this picks a random image from your site and
  redirects to this url.  The image can be anywhere in your site.

- ``@@randomcontent``: this picks a random content item from your site
  and redirects to this url.  The content must be in a specific
  folder, that you set in the control panel.

- ``@@randomsitecontent``: this picks a random content item from your
  site and redirects to this url.  The content can be anywhere in your
  site.


Compatibility
-------------

This is tested on Plone 4.2.  It will likely work on all 4.x versions.

It might work on Plone 3, but it uses ``plone.app.registry``, which is
not available by default, so you may need to take extra care about getting
versions of packages that work for your Plone version.  This is untested.


Authors
-------

- Maurits van Rees
