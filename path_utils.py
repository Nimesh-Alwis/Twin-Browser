import os
import sys

def get_app_dir():
    """
    Returns the application root directory.
    When running as a compiled PyInstaller executable (sys.frozen is True),
    this returns the directory containing the .exe file.
    When running as a script, this returns the directory containing path_utils.py.
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(os.path.abspath(sys.executable))
    else:
        return os.path.dirname(os.path.abspath(__file__))

def get_resource_path(relative_path):
    """
    Returns the absolute path to a bundled static resource file (read-only assets like HTML, icons, images).
    When frozen, PyInstaller extracts resources to sys._MEIPASS.
    """
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(get_app_dir(), relative_path)

def get_data_path(relative_path):
    """
    Returns the absolute path for user data files (bookmarks, notes, history, theme config, downloads).
    These are always stored in the app directory where the EXE is installed.
    """
    return os.path.join(get_app_dir(), relative_path)
