# Purpose

This is a demo of the Service Properties Parser utility, which was designed to resolve a set of troublesome issues for a support team in which updates to their peripheral services were time-intensive, convoluted, and prone to human error.

The use-case for this utility was particularly unique, but fun to explore. These Java-based peripheral services were dependent on .properties style config files which are uniques formatted compared to .ini config files. Further, new versions of these services would often have no config keys which - if not specified in the .properties file - would prevent the service from starting. Update files for new versions would contain and example .properties file with all required keys, but new keys were not explicitly labeled and complex and custom client-specific configurations would require a person to reconcile new and existing config keys and merge them in an updated file by hand.

This utility compiles all of the configuration keys for both the "current" properties file for a client or test environment and the default .properties file from the product repository for the "new" version selected in the user interace. After compiling the configuration keys, it runs a comparison between the two files. If there are configuration keys in "new" .properties that do not exist in the "current" properties file, the utility appends the key to the end of a copy of your provided .properties file. Config that exist in both "new" and "current" properties are not touched, ensuring that client preferences are not overwritten. Finally, if the key requires a profile tag prefix or a numbered suffix, the utility accounts for the current settings and updates the key accordingly.

## Goals

As an example of work done, here's a list of the original goals that fueled this project:

1. [x] Let user identify the version they're updating to
2. [x] Copy the new properties file to a temp location
3. [x] Compare the current agency properties to the default for the new version to look for new values
4. [x] If new values exist, append it to the end of the current properties using the default value


## Packaging and Delivering (Dev/DevOps/etc)

The Service Properties Parser utility was built with Python 3.7, but has been tested with Python 3.10. While we have the ability to create and deliver a folder with a Windows exe and binary dll files for our end-users to use, the Windows executable files will have to be built on a Windows machine with a Python interpreter and the pre-requisite libraries, and then the generated folder provided to end-users to run.

### Prerequisites for Building the Windows Executable

1. A Windows machine running at least Windows 7

2. [Python 3.7.3](https://www.python.org/downloads/release/python-373/) or higher

3. Installation of the required Python libraries  

Create a Python virtual environment to install the pre-requisite Python libraries. 

Then run pip install -r requirements.txt

### Using PyInstaller to Generate the Windows exe and binary files

Once the aforementioned prerequisites have been fufilled. You can use the download button to download a zip file of the source code to the Windows machine. Extract the downloaded source files and run the `run_pyinstaller.bat` to create the `build` and `dist` folders.

For most part, we can ignore the `build` folder, as its created while Pyinstaller builds the final distributable. The final folder will be inside of the `dist` folder. *As it stands right now, you cannot move the exe to a location separate from the other files in the named folder within `dist`. I don't consider it a huge deal as end-users can be given a shortcut if they'd rather initate the utility from the Desktop or such*

## How to Run the Application (end-user)

1. Select a product from the dropdown. For this demo, only "Demo" is available, but this menu was left unaltered to demonstrate what production use would look like
2. Select the version that you'd like to upgrade to. In "Demo" mode, there is no applicable version, however, production use would have queried a network repo to pull from a list of released dev versions
3. Browse to the location of your "current" .properties file. This file can be anywhere that is accessible on your machine, however - for ease, File Explorer will default to a sub-folder of the utility labeled `cur` (I couldn't resist).
4. Click the "Go" button and let the utility do it's thing.

## Notes

1. The .properties files in the "new" and "cur" folders are designed to give a surface-level demonstration of how the utility works. After running the utility, the .properties file in `output` should both show that existing config values were not altered - demonstrating that the utility is able to determine fulfilled requirements even when values, prefixes, or suffixes differ from the keys in the `_new.properties` file.
2. Both the .properties files and src files are commented to explain logic specifically useful to the original nuanced use-case
3. The modules have some functions and logic that are "useless" in a demo environment, however - again - they've been left to highlight how the utility is useful in a production use-case, and to reflect some unique code choices designed to make future expansion to other services and use-cases not as much of a pain in the butt (growth is cool)
