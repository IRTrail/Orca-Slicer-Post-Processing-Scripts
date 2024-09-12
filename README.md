
# Orca Slicer Post-Processing Scripts
*Post Processing Scripts for Orca Slicer*  
This is a collection of scripts for Orca Slicer that helps with things that Orca Slicer doesn't natively do. Most of these will be MMU centric, since that's where I find the most need.

## How to set up Orca Slicer to accept the script
1. Install Python.  
		You'll need to go [here](https://www.python.org/downloads/) and download the python installer of your choice and keep a note of where you put the executable.
2. Copy the path of the python executable. If it has spaces, you'll need to use double quotes (Windows) or the OS escape character in the path.
3. Put that in Orca Slicer in:
	"Others" > "Post-processing Scripts"
	![Python Executable Location Example](https://github.com/IRTrail/Orca-Slicer-Post-Processing-Scripts/blob/main/assets/python_executable.png?raw=true)
4. Copy the location you saved the script, put a space, then paste the path into Orca Slicer:
	![Python Script Location](https://github.com/IRTrail/Orca-Slicer-Post-Processing-Scripts/blob/main/assets/python_script.png?raw=true)
	
Now, it should edit your gcode files before exporting.
