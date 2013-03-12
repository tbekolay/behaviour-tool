set py_loc=C:\tbekolay\Python25\python.exe

%py_loc% Setup.py py2exe
mkdir dist\images
copy images\*.* dist\images\
copy BehaviourTool.chm dist\
