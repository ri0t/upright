Happy new year!
===============

You're probably (hopefully) looking at this in early January, because it's time
to update your copyright again, so have a good new year.

If not, maybe it's time to update your license text or your author's mail address?

Here it comes:

Upright - A sourcecode copyright maintenance tool
=================================================

This tool aims to support you in keeping your sourcecode copyright notices
up to date.

Right now, the tool focuses on Python code, but a lot of functionality is
very language independent. You could probably update copyright notices in svg
files or similar.

It analyses the headers of any given file tree to aid in fixing copyright issues.

Among those aids are:

- sorting and overviewing various copyright styles.
  Sometimes copyright notices are in docstrings. Sometimes, they're in comments, etc.
- check if any found copyright matches a template you supplied
- extract stats about outliers
- show headers of fishy files
- update various fields (mostly the year)
- insert templates

Howto
=====

Just supply a folder or run the tool in your destination folder.
It will only ever write to your files if you supply the "--write" flag.

Discover more options and operations by looking at the tool's --help page.

The command line interface has subgroups like `template` which have further sub-
commands listed. To get at them invoke it like `upright template --help` etc.

Maybe in 2021, I'll put up some more documentation. And a test suite.
And... aah... I sure hope i got you in the first half.

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

Copyright (C) 2017-2020 riot <riot@c-base.org>.

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
