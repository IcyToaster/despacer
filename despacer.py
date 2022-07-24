"""
Author: Natalie Smith
Date: 7/22/2022
Removes spaces from folders and files within a specified folder, 
    replacing each ' ' with '_'.
-F -> edit subfolder names
-f -> edit file names
-M -> don't edit main folder name
"""
#!/usr/bin/env python
import re
import sys
import os


def replaceSpaces(old_str):
    punct_str = re.compile(r' ')
    return punct_str.sub('_', old_str)


def splitPath(item_path):
    return (os.path.dirname(item_path), os.path.basename(item_path))


def searchFolder(new_path, update_folders, update_files):
    for item in os.listdir(new_path):
        new_item_path = os.path.join(new_path, item).replace("\\","/")
        # File
        if os.path.isfile(new_item_path) and update_files:
            new_file_name = os.path.join(new_path, replaceSpaces(item)).replace("\\", "/")
            os.rename(new_item_path, new_file_name)
            print(new_file_name)
        # Folder
        elif os.path.isdir(new_item_path) and update_folders:
            # Update folder name
            new_folder_name = os.path.join(new_path, replaceSpaces(item)).replace("\\", "/")
            os.rename(new_item_path, new_folder_name)
            print(new_folder_name)
            # Search newly renamed folder
            searchFolder(new_folder_name, update_folders, update_files)


if __name__ == '__main__':
    edit_subfolders = False
    edit_files = False
    edit_main_folder = True
    main_path_valid = True
    
    args = sys.argv[1:]
    for arg in args:
        if arg == "-f":
            edit_files = True
        elif arg == "-F":
            edit_subfolders = True
        elif arg == "-M":
            edit_main_folder = False

    main_folder_path = args[0]

    if not os.path.exists(main_folder_path):  # Check path validity
        print("Invalid path. Aborting.")
        main_path_valid = False

    if main_path_valid:
        new_main_path = main_folder_path

        # Edit folder name
        if edit_main_folder:
            main_folder_path_name = splitPath(main_folder_path)

            # Replace spaces in folder name
            replace_folder_name = replaceSpaces(main_folder_path_name[1])

            # Rename folder
            new_main_path = os.path.join(main_folder_path_name[0], replace_folder_name).replace("\\","/")
            os.rename(main_folder_path, new_main_path)
            print(new_main_path)

        # Rename subfolders and/or files
        if edit_files or edit_subfolders:
            searchFolder(new_main_path, edit_subfolders, edit_files)
