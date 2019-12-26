# BackuPy

https://github.com/elesiuta/backupy
https://pypi.org/project/BackuPy/

```
usage: backupy [-h] [-m mode] [-s mode] [-c mode] [--nomoves] [--noarchive]
               [--nolog] [--noprompt] [--norun] [--save] [--load]
               source [dest]

BackuPy: A succinct python program for backing up directories with an emphasis
on simple usage and transparent behavior

positional arguments:
  source       Path of source
  dest         Path of destination

optional arguments:
  -h, --help   show this help message and exit
  -m mode      Main mode:
               How to handle files that exist only on one side?
                 MIRROR (default)
                   [source-only -> destination, delete destination-only]
                 BACKUP
                   [source-only -> destination, keep destination-only]
                 SYNC
                   [source-only -> destination, destination-only -> source]
  -s mode      Selection mode:
               How to handle files that exist on both sides but differ?
                 SOURCE (default)
                   [copy source to destination]
                 DEST
                   [copy destination to source]
                 NEW
                   [copy newer to opposite side]
                 NO
                   [do nothing]
  -c mode      Compare mode:
               How to detect files that exist on both sides but differ?
                 ATTR (default)
                   [compare file attributes: mod-time and size]
                 BOTH
                   [compare file attributes first, then check CRC]
                 CRC
                   [compare CRC only, ignoring file attributes]
  --nomoves    Do not detect moved or renamed files
  --noarchive  Disable archiving files before overwriting/deleting to:
                 <source|dest>/.backupy/Archives/yymmdd-HHMM/
                 <source|dest>/.backupy/Trash/yymmdd-HHMM/
  --nolog      Disable writing to:
                 <source>/.backupy/Logs/log-yymmdd-HHMM.csv
                 <source|dest>/.backupy/database.json
  --noprompt   Complete run without prompting for confirmation
  --norun      Perform a dry run according to your configuration
  --save       Save configuration in source
  --load       Load configuration from source
```
