# -*- coding: utf-8 -*-
"""
API Kernel.

Expose the methods of the API kernel.

This API has multiple purposes:

* allow the application manipulation via low-level methods (in *shell script*)
* define a profile API for each route
   * each route will then have the same profile on every API channel (Python, REST and Django-shell)
"""
from .install import install
from .create_superuser import create_superuser
