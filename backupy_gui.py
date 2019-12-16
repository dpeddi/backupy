import sys
import typing
import PySimpleGUI as sg
from colored import stylize, attr, fg
from gooey import Gooey, GooeyParser
import backupy

def colourize(string: str, colour: str) -> str:
    return string
    
def simplePrompt(msg: str) -> str:
    sg.change_look_and_feel('System Default For Real')
    layout = [ [sg.Text(msg)],
               [sg.Button('Ok'), sg.Button('Cancel')] ]
    window = sg.Window('BackuPy', layout)
    event, _ = window.Read()
    window.close()
    if event == "Ok":
        return "y"
    else:
        return "n"

@Gooey(program_name="BackuPy", richtext_controls=False, tabbed_groups=True)
def main_gui():
    # load profiles
    dict_profiles = backupy.readJson("profiles.json")
    if "profiles" in dict_profiles:
        list_profiles = dict_profiles["profiles"]
    else:
        list_profiles = []
    # argparse setup
    parser = GooeyParser(description="A simple python program for backing up directories")
    group1 = parser.add_argument_group("Profiles", "")
    group2 = parser.add_argument_group("Directories", "")
    group3 = parser.add_argument_group("Configuration", "")
    group1.add_argument("--loadprofile", metavar="Load Saved Profile", nargs="*", widget="Listbox", choices=list_profiles,
                        help="Load a previously saved profile")
    group2.add_argument("--source", action="store", type=str, default=None, widget="DirChooser", gooey_options={"full_width":True},
                        help="Path of source")
    group2.add_argument("--dest", action="store", type=str, default=None, widget="DirChooser", gooey_options={"full_width":True},
                        help="Path of destination")
    group3_main = group3.add_mutually_exclusive_group(required=True,
                                                      gooey_options={"title":"Main mode: How to handle files that exist only on one side?",
                                                                     "full_width":True,
                                                                     'initial_selection':0})
    group3_main.add_argument("--main_mirror", metavar="Mirror", action="store_true",
                             help="[source-only -> destination, delete destination-only]")
    group3_main.add_argument("--main_backup", metavar="Backup", action="store_true",
                             help="[source-only -> destination, keep destination-only]")
    group3_main.add_argument("--main_sync", metavar="Sync", action="store_true",
                             help="[source-only -> destination, destination-only -> source]")
    group3_select = group3.add_mutually_exclusive_group(required=True,
                                                        gooey_options={"title":"Selection mode: How to handle files that exist on both sides but differ?",
                                                                       "full_width":True,
                                                                       'initial_selection':0})
    group3_select.add_argument("--select_source", metavar="Source", action="store_true",
                               help="[copy source to destination]")
    group3_select.add_argument("--select_dest", metavar="Destination", action="store_true",
                               help="[copy destination to source]")
    group3_select.add_argument("--select_new", metavar="New", action="store_true",
                               help="[copy newer to opposite side]")
    group3_select.add_argument("--select_no", metavar="None", action="store_true",
                               help="[do nothing]")
    group3_compare = group3.add_mutually_exclusive_group(required=True,
                                                         gooey_options={"title":"Selection mode: How to handle files that exist on both sides but differ?",
                                                                        "full_width":True,
                                                                        'initial_selection':0})
    group3_compare.add_argument("--compare_attr", metavar="Attributes", action= "store_true",
                                help="[compare file attributes: mod-time and size]")
    group3_compare.add_argument("--compare_both", metavar="Both", action= "store_true",
                                help="[compare file attributes first, then check CRC]")
    group3_compare.add_argument("--compare_crc", metavar="CRC", action= "store_true",
                                help="[compare CRC only, ignoring file attributes]")
    group3.add_argument("--nomoves", action="store_true",
                        help="Do not detect moved or renamed files")
    group3.add_argument("--noarchive", action="store_true",
                        help="Disable archiving files before deleting/overwriting to:\n"
                             "  <source|dest>/.backupy/yymmdd-HHMM/\n")
    group3.add_argument("--nolog", action="store_true",
                        help="Disable writing to:\n"
                             "  <source>/.backupy/log-yymmdd-HHMM.csv\n"
                             "  <source|dest>/.backupy/database.json")
    group3.add_argument("--noprompt", action="store_true",
                        help="Complete run without prompting for confirmation")
    group3.add_argument("--norun", action="store_true",
                        help="Perform a dry run according to your configuration")
    group2.add_argument("--save", action="store_true",
                        help="Save configuration in source")
    group2.add_argument("--load", action="store_true",
                        help="Load configuration from source")
    # parse args and store dictionary
    args = vars(parser.parse_args())
    args["stdout_status_bar"] = False # https://github.com/chriskiehl/Gooey/issues/213 , use a simpler expression and hide_progress_msg
    # convert radio groups back to choice of string
    if args["main_mirror"] == True:
        args["main_mode"] = "mirror"
    elif args["main_backup"] == True:
        args["main_mode"] = "backup"
    elif args["main_sync"] == True:
        args["main_mode"] = "sync"
    if args["select_source"] == True:
        args["select_mode"] = "source"
    elif args["select_dest"] == True:
        args["select_mode"] = "dest"
    elif args["select_new"] == True:
        args["select_mode"] = "new"
    elif args["select_no"] == True:
        args["select_mode"] = "no"
    if args["compare_attr"] == True:
        args["compare_mode"] = "attr"
    elif args["compare_both"] == True:
        args["compare_mode"] = "both"
    elif args["compare_crc"] == True:
        args["compare_mode"] = "crc"
    # store profile if new
    if args["save"] and args["source"] not in list_profiles:
        list_profiles.append(args["source"])
        backupy.writeJson("profiles.json", {"profiles": list_profiles}, False)
    # execute selected profiles or config
    if args["loadprofile"] != []:
        for i in range(len(args["loadprofile"])):
            args["source"] = args["loadprofile"][i]
            args["load"] = True
            backup_manager = backupy.BackupManager(args, gui=True)
            backup_manager.backup()
    else:
        backup_manager = backupy.BackupManager(args, gui=True)
        backup_manager.backup()


if __name__ == "__main__":
    sys.exit(main_gui())


# TODO
# About dialog - https://github.com/chriskiehl/Gooey#menus
# Richtext - https://github.com/chriskiehl/GooeyExamples/blob/master/examples/richtext_demo.py
# add gui imports (functions from here) to BackupManager init if gui
# use radio group for mode (needs testing, title use in gooey-options is undocumented)
# build with onedir and create installer with inno setup - https://github.com/jrsoftware/issrc
