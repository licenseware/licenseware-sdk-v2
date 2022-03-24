"""

Here are package static files that are used by the cli to generate files and folders.
We are using jinja2 to fill variables from files.


Usage: 

```py

import pandas as pd

from licenseware import resources
import importlib.resources as pkg_resources



file_bytes_io = pkg_resources.open_binary(resources, 'filename_from_resources_package.csv')
df = pd.read_csv(file_bytes_io)

# pkg_resources has available also these useful methods: read_text, path


```

See more in docs:
[resources-docs](https://docs.python.org/3/library/importlib.html#module-importlib.resources)


Prefix all `.py` template files with an underscore `_main.py` that's to tell pdoc3 to ignore them. 

"""
