#!/usr/bin/python

"""
This is a script to create the bones of a Flask application using Python.

The created structure is as follows, for an app named foo:

~/foo
  |
  __/foo_app
  |     |-- __init__.py
  |     |-- models.py
  |     |-- views.py
  |     |__ /static
  |     |__ /templates
  |         |__foo
  |             |-- index.html
  |         
  |--run.py
  |__/venv

"""

import os
import sys, getopt

verbose=False

def create_app(app_name, root_dir):
  """Create the application."""
  debug('Creating a new Flask app [%s] at location [%s]' % (app_name, root_dir))

  # Create the project directory.
  project_dir = create_dir(root_dir, app_name)

  #Create the virtual environment.
  create_venv(project_dir)

  app_dir_name = app_name + '_app'

  #Create the run script and a blank config
  create_run_script(project_dir, app_dir_name)
  create_file(project_dir, 'config.py')

  #Create the app directory and init file
  app_dir = create_dir(project_dir, app_dir_name)
  create_init_script(app_dir, app_dir_name)

  #Create the models, views and forms files
  create_file(app_dir, 'models.py')
  create_file(app_dir, 'forms.py')
  create_views_script(app_dir, app_dir_name)

  #Create the static directory
  static_dir = create_dir(app_dir, 'static')

  #Create the templates
  templates_dir = create_dir(app_dir, 'templates')
  templates_mod_dir = create_dir(templates_dir, app_name)
  create_basic_view(templates_mod_dir, app_name)
  debug('Finished app creation.')

def create_basic_view(templates_dir, app_name):
  """Creates a basic index page."""
  index_page = create_file(templates_dir, 'index.html')
  lines = []
  lines.append('<html>')
  lines.append('<head><title>%s - Index</title></head>' % app_name)
  lines.append('<body>This is a default page for project <b>%s</b>. Now do \
    something.</body>' % app_name)
  lines.append('</html>')
  write_to_file(index_page, lines)
  debug('Created index page.')

def create_views_script(app_dir, app_dir_name):
  """Creates views.py"""
  view_script = create_file(app_dir, 'views.py')
  lines = []
  lines.append('from flask import render_template')
  lines.append('from %s import app' % app_dir_name)
  lines.append('')
  lines.append('@app.route(\'/\', methods=[\'GET\'])')
  lines.append('def render_index():')
  lines.append('\treturn render_template(\'%s/index.html\')' % app_dir_name[:-4])
  write_to_file(view_script, lines)
  debug('Created view script.')

def create_init_script(app_dir, app_dir_name):
  """Creates the init script."""
  init_script = create_file(app_dir, '__init__.py')
  lines = []
  lines.append('from flask import Flask')
  lines.append('')
  lines.append('app = Flask(__name__)')
  lines.append('')
  lines.append('from %s import views' % app_dir_name)
  lines.append('app.config.from_object("config")')
  write_to_file(init_script, lines)
  debug('Created init script.')

def create_run_script(project_dir, app_dir_name):
  """Creates the run script."""
  run_script = create_file(project_dir, 'run.py')
  lines = []
  lines.append('#!flask/bin/python')
  lines.append('from %s import app' % app_dir_name)
  lines.append('app.run(debug=True)')
  write_to_file(run_script, lines)
  debug('Created run script.')

def write_to_file(file, lines):
  """Writes an array of lines to a file."""
  file_handle = open(file, 'w')
  for line in lines:
    file_handle.write(line + '\n')
  file_handle.close()

def create_venv(app_root):
  """Create the virtual environment directory."""
  venv_dir = create_dir(app_root, 'venv')
  debug('Created the virtual environment directory.')

def create_file(path, new_file_name):
  """Create a new file."""
  if not os.path.exists(path):
    raise Exception('Path [%s] does not exist.' % path)
  to_create = os.path.join(path, new_file_name)
  if os.path.exists(to_create):
    raise Exception('File [%s] already exists.' % to_create)
  new_file = open(to_create, 'w')
  new_file.close()
  return to_create

def create_dir(path, new_dir_name):
  """Create a directory and return its path."""
  if not os.path.exists(path):
    raise Exception('Path [%s] does not exist.' % path)
  to_create = os.path.join(path, new_dir_name)
  if os.path.exists(to_create):
    raise Exception('Folder [%s] already exists.' % to_create)
  os.makedirs(to_create)
  debug('Created directory [%s]' % to_create)
  return to_create

def usage():
  """Prints a usage guide."""
  print 'Usage: python create_flask_app.py app_name [root_dir]'

def debug(debug_str):
  """Prints only if verbose is on."""
  if verbose:
    print debug_str

def main(argv):
  """Main method."""
  app_name = ''
  root_dir = os.getcwd()

  try:
    opts, args = getopt.getopt(argv, 'v')
  except getopt.GetoptError:
    usage()
    sys.exit(2)

  for opt, arg in opts:
    if opt == '-v':
      global verbose   
      verbose = True
  
  if not args or len(args) > 2:
    # Wrong number of arguments supplied.
    usage()
    sys.exit(2)
  else:
    app_name = args[0].lower()
    if len(args) == 2:
      root_dir = os.path.abspath(args[1])

  create_app(app_name, root_dir)

if __name__ == '__main__': main(sys.argv[1:])