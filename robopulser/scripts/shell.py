try:
    import importlib.resources as resources
except ImportError:
    import importlib_resources as resources

import os, shutil
from . import templates

def copy_templates():
    
    templates_dir = templates.__path__[0]
    
    yml_filename = "example.yml"
    yml_file_full_pth = os.path.join(templates_dir, yml_filename)

    py_filename = "pulser.py"
    py_file_full_pth = os.path.join(templates_dir, py_filename)

    shutil.copyfile(yml_file_full_pth, yml_filename)
    print(f"Got template: {yml_filename}")
    shutil.copyfile(py_file_full_pth, py_filename)
    print(f"Got template: {py_filename}")

if __name__ == "__main__":
    copy_templates()