#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

# Upright - A sourcecode copyright maintenance tool
# =================================================
# Copyright (C) 2017-2020 riot <riot@c-base.org>
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

from setuptools import setup, find_packages
import os

setup(
    name="upright",
    description="A sourcecode copyright maintenance tool",
    version="0.0.2",
    author="Heiko 'riot' Weinen",
    author_email="riot@c-base.org",
    maintainer="Heiko 'riot' Weinen",
    maintainer_email="riot@c-base.org",
    url="https://github.com/ri0t/upright",
    license="GNU General Public License v3",
    scripts=['upright'],
    long_description="""Upright - A sourcecode copyright maintenance tool
    =================================================

    This tool aims to support you in keeping your sourcecode copyright
    notices up to date.

    Right now, the tool focuses on Python code.

    See https://github.com/ri0t/upright""",
    dependency_links=[
    ],
    install_requires=[
        'pystache>=0.5.4',
        'click>=6.7.0',
        'click-didyoumean>=0.0.3'
    ],
    test_suite="tests.main.main",
)
