# BackuPy
## Installation
- Install the latest release from PyPI (supports all platforms with Python and has no other dependencies)
```
pip install backupy --upgrade
```
- GUI version is also available by installing BackuPy-Setup.exe from the GitHub releases page
- The GUI can also be run directly from backupy_gui.py and packaged for other operating systems
## Features
- Backup, Mirror, and Sync Modes
- Compare files using attributes or CRCs
- Detection and alerts of corrupted files
- JSON formatted database for tracking files and csv formatted logs
- Detection and alerts of unexpected file modifications on destination outside of backups and mirrors, or sync conflicts (a file was modified on both sides since the last sync)
- Files are always copied to an identically structured archive directory before being deleted or overwritten by default
- Save and load your configuration
- Perform a dry run to test your configuration
- Works on both new and existing backup directories
- Filter file paths with regular expressions
## Under the Hood
- Easy to use in scripts (see backupy_batch.py for an example)
- Clear and easy to verify code, the only functions that touch your files are: copyFile(), moveFile(), and  removeFile()
- Very simple design and only uses the Python standard library for fewer points of failure
## Usage Description
- Source and destination directories can be any accessible directory (mounted drives, cloud storage, Syncthing folders, etc)
- Destination can be empty or contain files from a previous backup, matching files on both sides will be skipped
- Main modes (how to handle new and deleted files)
  - Backup mode: copies files that are only in source to destination
  - Mirror mode: copies files that are only in source to destination and deletes files that are only in destination
  - Sync mode: copies files that are only in source to destination and copies files that are only in destination to source
- Selection modes (which file to select in cases where different versions exist on both sides)
  - Source mode: copy source files to destination
  - Destination mode: copy destination files to source
  - Newer mode: copy newer files based on last modified time
  - None mode: don't copy either, differing files will only be logged for manual intervention
- Compare modes (how to detect which files have changed)
  - Attribute mode: compare file attributes (size and last modified time)
  - Attribute+ mode: compare file attributes and calculate CRCs only for new and changed files for future verification
  - CRC mode: compare file attributes and CRC for every file, and checks previously stored CRCs to detect corruption
- Test your settings first with the 'dry-run' flag
## Example Usage
- Just type backupy followed by your source and destination directories, and any combination of options
- If you're unsure how something works, include "--dry-run" to see what would happen without actually doing anything
```
backupy "path/to/your/source directory/" "path/to/destination/" --dry-run
```
## Command Line Interface
```
usage: backupy [options] -- <source> <dest>
       backupy <source> <dest> [options]
       backupy <source> --load [-c mode] [--dbscan] [--dry-run]
       backupy -h | --help

BackuPy: A simple backup program in python with an emphasis on data integrity
and transparent behaviour

positional arguments:
  source       Path to source
  dest         Path to destination

optional arguments:
  -h, --help   show this help message and exit

file mode options:

  -m mode      Main mode: for files that exist only on one side
                 MIRROR (default)
                   [source-only -> destination, delete destination-only]
                 BACKUP
                   [source-only -> destination, keep destination-only]
                 SYNC
                   [source-only -> destination, destination-only -> source]
  -s mode      Selection mode: for files that exist on both sides but differ
                 SOURCE (default)
                   [copy source to destination]
                 DEST
                   [copy destination to source]
                 NEW
                   [copy newer to opposite side]
                 NO
                   [do nothing]
  -c mode      Compare mode: for detecting which files differ
                 ATTR (default)
                   [compare file attributes: mod-time and size]
                 ATTR+
                   [compare file attributes and record CRC for changed files]
                 CRC
                   [compare file attributes and CRC for every file]

misc file options:

  --fi regex [regex ...]
               Filter: Only include files matching the regular expression(s)
               (include all by default, searches file paths)
  --fe regex [regex ...]
               Filter: Exclude files matching the regular expression(s)
               (exclude has priority over include, searches file paths)
  --noarchive  Disable archiving files before overwriting/deleting to:
                  <source|dest>/.backupy/Archives/yymmdd-HHMM/
                  <source|dest>/.backupy/Trash/yymmdd-HHMM/
  --nomoves    Do not detect when files are moved or renamed

execution options:

  --noprompt   Complete run without prompting for confirmation
  -d, --dbscan
               Only scan files to check and update their database entries
  -n, --dry-run
               Perform a dry run with no changes made to your files
  -q, --qconflicts
               Quit if database conflicts are detected (always notified)
                 -> unexpected changes on destination (backup and mirror)
                 -> sync conflict (file modified on both sides since last sync)
                 -> file corruption (ATTR+ or CRC compare modes)
  -v, --verify
               Verify CRC of copied files

configuration options:

  --nolog      Disable writing log and file databases to:
                  <source>/.backupy/Logs/log-yymmdd-HHMM.csv
                  <source|dest>/.backupy/database.json
  -p, --posix  Force posix style paths on non-posix operating systems
  -k, --save   Save configuration to <source>/.backupy/config.json
  -l, --load   Load configuration from <source>/.backupy/config.json
```
## Extra Configuration Options
- Some options can only be set from the config.json file
  - archive_dir
    - can be any subdirectory, default = ".backupy/Archive"
  - config_dir
    - can't be changed under normal operation, default = ".backupy"
  - log_dir
    - can be any subdirectory, default = ".backupy/Logs"
  - trash_dir
    - can be any subdirectory, default = ".backupy/Trash"
  - cleanup_empty_dirs
    - delete directories when they become empty, default = True 
  - root_alias_log
    - replace source and dest paths with "\<source\>" and "\<dest\>" in logs, default = True
  - stdout_status_bar
    - show progress status bar, default = True
  - verbose
    - print program status updates to stdout, default = True
## Building From Source
- Run tests with
```
python setup.py test
```
- Building a python package
```
python setup.py sdist
```
- Building an executable with the GUI
```
pyinstaller build.spec
```
- You can package the executable on Windows by running setup.iss with Inno Setup
## Links
- https://github.com/elesiuta/backupy
- https://pypi.org/project/BackuPy/
