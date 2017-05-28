.. image:: https://travis-ci.org/ri0t/upright.svg?branch=master
:target: https://travis-ci.org/ri0t/upright
    :alt: Build Status

.. image:: https://landscape.io/github/ri0t/upright/master/landscape.svg?style=flat
:target: https://landscape.io/github/ri0t/upright/master
    :alt: Quality

.. image:: https://coveralls.io/repos/ri0t/upright/badge.svg
:target: https://coveralls.io/r/ri0t/upright
    :alt: Coverage

.. image:: https://requires.io/github/ri0t/upright/requirements.svg?branch=master
:target: https://requires.io/github/ri0t/upright/requirements/?branch=master
    :alt: Requirements Status


Upright - A sourcecode copyright maintenance tool
=================================================

This tool aims to support you in keeping your sourcecode copyright notices
up to date.

Right now, the tool focuses on Python code.

It analyses the headers of any given file tree to

- first sort the various styles you have
- check if any found copyright matches a template you supplied
- update various fields (mostly the year)

Howto
=====

Just supply a folder or run the tool in your destination folder.
It will only ever write to your files if you supply the "--write" flag.

Discover more options etc by looking at the tool's --help page.

Bugs & Discussion
=================

Please research any bugs you find via our `Github issue tracker for
upright <https://github.com/ri0t/upright/issues>`__ and report them,
if they're still unknown.

Contributors
============

We like to hang out on irc, if you want to chat or help out,
join irc://freenode.org/hackerfleet :)

Please be patient or even better use screen/tmux or something to irc.
Most of us are there 24/7 but not always in front of our machines.

Missing in the list below? Add yourself or ping us ;)

Code
----

-  Heiko 'riot' Weinen riot@c-base.org

License
=======

Copyright (C) 2017 riot <riot@c-base.org>.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
