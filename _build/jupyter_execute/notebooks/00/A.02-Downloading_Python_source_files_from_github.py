#!/usr/bin/env python
# coding: utf-8

# # Downloading Python source files from github
# 
# This project incorporates Python modules and functions that are used in multiple notebooks. Most of these are  simple convenience functions for accessing device hardware. But whatever the use, repeating the same source code in multiple notebooks complicates maintenance and has little value for the reader. For these reasons, it is much better to maintain code in the project's repository and import as needed for use in the notebooks. 
# 
# Unfortunately, Github stores code files in an a database for which the standard API does not provide direct access to whole directories. There are libraries circulating in the Python community designed to circumvent this limitation. 
# 
# Here we demonstrate three techniques:
# 
# 1. Use of `wget` to selectively download individual Python source files to the current working directory.
# 2. The use of `git clone` to download the entire repository and then add a Python source directory to the import path. Changes to the code can be committed and pushed back to the git repository.
# 3. Use of `pip  install` to install python packages from a githb repository. This is convenient for the notebook user, but requires a properly configured `setup.py` in the repository. 

# 
# ## Method 1. Downloading individual Python files with wget
# 
# The file `hello_world.py` is located in the top-level `src` directory of a github repository. To access the file, use the shell command `wget` with an `https` link to the raw content of the main branch. The prefix exclamation/bang symbol `!` causes the following line to be executed by the system command line rather than the Python kernal. The `--no-cache` option ensures the latest version is downloaded. 
# 
# The `--backups=1` option saves any prior version of the same code file to a backup.

# In[ ]:


user = "jckantor"
repo = "cbe-virtual-laboratory"
src_dir = "src"
pyfile = "hello_world.py"

url = f"https://raw.githubusercontent.com/{user}/{repo}/main/{src_dir}/{pyfile}"
get_ipython().system('wget --no-cache --backups=1 {url}')


# In[ ]:


import subprocess

result = subprocess.run(["wget", "--no-cache", "--backups=1", url], stderr=subprocess.PIPE, stdout=subprocess.PIPE)
print(result.stderr.decode("utf-8"))


# Let's make a listing of the file's content.

# In[ ]:


with open(pyfile, 'r') as f:
    print(f.read())


# Let's import the file as a Python module and use the embedded functions. If the name of the file is fixed and known, then the usual Python `import` statement will do the job.

# In[ ]:


import hello_world
help(hello_world)
hello_world.hello()


# If the name of the python file is given as the value of a Python string variable then the standard library `importlib` may be used. Note the need to strip any suffix from a file name.

# In[ ]:


import importlib
mymodule = importlib.import_module(pyfile.rstrip(".py"))
help(mymodule)
mymodule.hello()


# For platforms where the shell escape `!` might fail, an alternative is to use the standard Python `subprocess` library.

# ## Method 2. Cloning a git repository
# 
# Downloading a collection of files from a git repository with `wget` (or `curl`) can be cumbersome, particularly if the names of the individual files are unknown or subject to change. And, unfortunately, Github does not provide an API for accessing a folder of files. 
# 
# For these situations, an alternative is to simply clone the git repository to to a local directory. 

# In[ ]:


import os

user = "jckantor"
repo = "cbe-virtual-laboratory"

# remove local directory if it already exists
if os.path.isdir(repo):
    get_ipython().system('rm -rf {repo}')

get_ipython().system('git clone https://github.com/{user}/{repo}.git')


# With the repository cloned to a local subdirectory of the same name, there are several useful strategies for importing from the source directory. The following cell demonstrates how to insert a repository source directory in Python path (if it doesn't appear already).

# In[ ]:


import sys

src_dir = "src"

path = f"{repo}/{src_dir}"
if not path in sys.path:
    sys.path.insert(1, path)

# list all directories in the Python path
print("\n".join(["'" + path + "'" for path in sys.path]))


# The next stop is to import a python module from inside the library

# In[ ]:


import sys

src_dir = "src"

sys.path.insert(1, f"{repo}/{src_dir}")
import hello_world
hello_world.hello()


# The following cell summaries these steps into a single cell that can be copied into a new notebook.

# In[ ]:


import os, sys, importlib

user = "jckantor"
repo = "cbe-virtual-laboratory"
src_dir = "src"
pyfile = "hello_world.py"

if os.path.isdir(repo):
    get_ipython().system('rm -rf {repo}')

get_ipython().system('git clone https://github.com/{user}/{repo}.git')

path = f"{repo}/{src_dir}"
if not path in sys.path:
    sys.path.insert(1, path)

mymodule = importlib.import_module(pyfile.rstrip(".py"))
help(mymodule)


# ### Commit and push changes
# 
# A potential use case for cloning a repository is to allow for editing the source code directly from a Jupyter notebook. In this case, the code can be committed and pushed back to the reposity using standard `git` commands. 
# 
# Be sure you know what you're doing before attempting this. This code has been commented out to avoid inadvertent changes to this repository's source code.

# In[ ]:


import os
from getpass import getpass
import urllib

#password = getpass('Password: ')
#password = urllib.parse.quote(password)

#cmd_str = f"git -C https://{user}:{password}@github.com/{user}/{repo} push"
#os.system(cmd_string)

#!git -C /content/cbe-virtual-laboratory commit -m "update"
#!git -C /content/cbe-virtual-laboratory push

#cmd_str, password = "", "" # removing the password from the variable


# ## Method 3. Using pip to install from a github repository
# 
# The methods presented above assume the user has detailed knowledge of how functions have been organized into modules in the repository's source directory. For simple applications, that may be satisfactory and those methods are fast and can work well. For more complex applications, however, it will be helpful to use common methods for creating Python software packages. 
# 
# For this case we assume a file `setup.py` has been included in the top-level directory of the repository that specifies how packages have been organized into source directories following using the [setuptools](https://setuptools.readthedocs.io/en/latest/) library.
# 
# Assuming `setup.py` is present and that the usual conventions for creating Python packages have been followed, the packages can be loaded directory from github as shown in the following cell.

# In[ ]:


user = 'jckantor'
repo = 'cbe-virtual-laboratory'

url = f"git+https://github.com/{user}/{repo}.git"
get_ipython().system('pip install --upgrade {url}')


# In[ ]:


from cbelaboratory.hello_world import hello
hello()


# ## Summary and recommended practices
# 
# Which of these methods should one use? While there is overlap in the functionality, there are some recommendations that can be make.
# 
# * If you need to import just a few python files, the `wget` methd is easy to use and minimizes the amount of transmitted data.
# 
# * If you wish to import a whole folders of source code, creating a local clone of the repository is easy to code with `git`. Moveover, it is possible to edit, commit, and push code back to the repository directory from a notebook.
# 
# * For more complex projects where organization of the source code should decoupled from it's use, the conventional packaging methods of Python should be used. The packages can be install from the github repository using `pip`.
