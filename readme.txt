Behaviour Tool v 0.0.1 by Trevor Bekolay

The necessary files to create BehaviourTool.chm are in the docs/ directory;
use Microsoft HTML Help to open up the project file and recompile the .chm file
if changes are made that would require the documentation to be updated.

To generate a Win32 executable (for machines that do not have python or wxPython
installed), run build.bat. Be sure to change the location of python.exe in
build.bat to reflect your environment. The files needed to run the program will
be in the dist/ directory.  If the .chm file exists, it will be copied to this
folder as well.
