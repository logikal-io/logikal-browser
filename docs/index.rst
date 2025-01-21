.. Documentation structure
.. toctree::
    :caption: Documentation
    :hidden:

    self
    browser
    scenarios
    development
    license

.. toctree::
    :caption: External Links
    :hidden:

    Release Notes <https://github.com/logikal-io/logikal-browser/releases>
    Issue Tracker <https://github.com/logikal-io/logikal-browser/issues>
    Source Code <https://github.com/logikal-io/logikal-browser>

Getting Started
===============
.. contents::
    :local:
    :depth: 1

Introduction
------------
The logikal-browser package provides a convenient high-level interface for web browser management
and automation (with `Selenium <https://www.selenium.dev/>`_). First, define the appropriate
browser versions that should be used in your ``pyproject.toml`` file:

.. code-block:: toml

    [tool.browser.versions]
    chrome = '130.0.6723.69'
    edge = '129.0.2792.65'

Then create the desired :class:`~logikal_browser.Browser` sub-class instance:

.. code-block:: python

    from logikal_browser.chrome import ChromeBrowser
    from logikal_browser.scenarios import desktop

    browser = ChromeBrowser(settings=desktop.settings)
    browser.get('https://logikal.io')
    browser.check()

That's it! The correct web browser and web driver will be automatically installed, and the enhanced
:class:`~selenium.webdriver.remote.webdriver.WebDriver` instance can be used straightaway.

Installation
------------
You can simply install ``logikal-browser`` from `pypi
<https://pypi.org/project/logikal-browser/>`_:

.. code-block:: shell

    pip install logikal-browser

.. note:: If your system uses AppArmor, you may need to add a `new profile
    <https://chromium.googlesource.com/chromium/src/+/main/docs/security/apparmor-userns-restrictions.md>`_
    that allows unconfined execution of the developer build browser binaries. For example, in the
    case of Chrome:

    .. code-block:: ini

        # Based on /etc/apparmor.d/chrome
        abi <abi/4.0>,
        include <tunables/global>

        profile chrome-dev /@{HOME}/.cache/logikal_browser/chrome/**/chrome flags=(unconfined) {
            userns,

            include if exists <local/chrome>
        }

Extras
------
django
~~~~~~
The Django extra provides the necessary requirements for the :func:`logikal_browser.Browser.login`
method:


.. code-block:: shell

    pip install logikal-browser[django]
