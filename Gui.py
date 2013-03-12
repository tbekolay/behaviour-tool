# Copyright (c) 2010, Trevor Bekolay
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without modification,
# are permitted provided that the following conditions are met:
#
#    * Redistributions of source code must retain the above copyright notice, this
#      list of conditions and the following disclaimer.
#    * Redistributions in binary form must reproduce the above copyright notice, this
#      list of conditions and the following disclaimer in the documentation and/or other
#      materials provided with the distribution.
#    * Neither the name of the IRCL nor the names of its contributors may be used to
#      endorse or promote products derived from this software without specific prior
#      written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY
# EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT
# OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR 
# TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE,
# EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

# System imports
import os, sys, wx
import ConfigParser
import wx.lib.mixins.listctrl as listmix
import wx.lib.ogl as ogl
import wx.stc

# Behaviour tool imports
import Codegen, Io

class Model(object):
    """The Model keeps track of all of the data that the GUI needs.
    
    This includes the actual behaviour that the GUI is working on, as well as
    lists that combo boxes will need, and other miscellaneous pieces of data
    that are used more than once in different areas of the GUI."""
    def __init__(self):
        """Sets up the instance variables."""
        self.behaviour = Codegen.Behaviour()
        """The behaviour object that the GUI displays and modifies.
        @type: L{Behaviour}
        """
        self.actual_verbs = []
        """The actual verbs that are defined in C{util_verbs.nss}.
        @type: list of L{ActualVerb}s
        """
        self.actual_verb_names = []
        """The names of the actual verbs stored in actual_verbs.
        
        While this information is somewhat redundant, it is used by a combo box 
        on each verb panel, so it is useful to maintain.
        @type: list of strings
        """
        self.verb_names = []
        """The contextual names of the verbs stored in the behaviour object.
        
        While this information is somewhat redundant, it is used by follower
        dropdown boxes, so it is useful to maintain.
        @type: list of strings
        """
        self.object_names = []
        """The names of all actors and variables of type 'object'.
        
        While this information is somewhat redundant, it is used by combo boxes
        on the verb panel, so it is useful to maintain.
        @type: list of strings
        """
        self.string_names = []
        """The names of all variables of type 'string'.
        
        While this information is somewhat redundant, it is used by combo boxes
        on the verb panel, so it is useful to maintain.
        @type: list of strings
        """        
        self.int_names = []
        """The names of all variables of type 'int'.
        
        While this information is somewhat redundant, it is used by combo boxes
        on the verb panel, so it is useful to maintain.
        @type: list of strings
        """
        self.float_names = []
        """The names of all variables of type 'float'.
        
        While this information is somewhat redundant, it is used by combo boxes
        on the verb panel, so it is useful to maintain.
        @type: list of strings
        """
        self.space = 3
        """The amount of space between widgets in the GUI.
        @type: int
        """
        self.desc_length = 20
        """The maximum length a string can be before it is cut off in a
        trash popup menu.
        @type: int
        """
        
        # Fonts
        self.title_font = None
        """The font used for the titles of sections.
        @type: wx.Font
        """
        self.shape_font = None
        """The font used for the text in verb shapes on the L{VerbCanvas} OGL object.
        @type: wx.Font
        """
        
        # Bitmaps
        self.refresh_bmp = None
        """The bitmap used for refresh BitmapButtons.
        @type: wx.Bitmap
        """
        self.trash_bmp = None
        """The bitmap used for trash BitmapButtons.
        @type: wx.Bitmap
        """
        self.add_bmp = None
        """The bitmap used for add BitmapButtons.
        @type: wx.Bitmap
        """
        self.del_bmp = None
        """The bitmap used for delete BitmapButtons.
        @type: wx.Bitmap
        """
        self.del_verb_bmp = None
        """The bitmap used for the verb deletion BitmapButton.
        @type: wx.Bitmap
        """
        self.open_bmp = None
        """The bitmap used for open BitmapButtons.
        @type: wx.Bitmap
        """
    
    def UpdateActualVerbNames(self):
        """Updates the actual verb names list (actual_verb_names) that combo boxes use.
        
        This should be called any time a change is made to the actual_verbs list."""
        self.actual_verb_names = []
        for verb in self.actual_verbs:
            self.actual_verb_names.append(verb.name)
    
    def UpdateVerbNames(self):
        """Updates the verb names list that combo boxes use.
        
        This should be called any time the contextual name of a verb in the
        behaviour object is changed, or a verb is added or removed."""
        self.verb_names = []
        for verb in self.behaviour.verbs:
            self.verb_names.append(verb.context_name)
    
    def UpdateNWVarNames(self):
        """Updates the four lists concerning NWVariable names that combo boxes use.
        
        This should be called any time an NWVariable's name changes, or an
        NWVariable is added or removed."""
        self.object_names = []
        self.string_names = []
        self.int_names = []
        self.float_names = []
        
        for nwvar in self.behaviour.nwvariables:
            if nwvar.type == "object":
                self.object_names.append(nwvar.name)
            elif nwvar.type == "string":
                self.string_names.append(nwvar.name)
            elif nwvar.type == "int":
                self.int_names.append(nwvar.name)
            elif nwvar.type == "float":
                self.float_names.append(nwvar.name)
    
    def LoadUtilVerbs(self, path):
        """Try to load the C{util_verbs.nss} file at the given path.
        @param path: Path to the C{util_verbs.nss} file.
        @type path: string
        """
        self.actual_verbs = Io.LoadActualVerbs(path)
        self.UpdateActualVerbNames()

# Make a global model and config to be used by the GUI.
#  We could instead pass this object to each widget, but the model is in the gui
#  namespace, so its scope remains in the gui anyway.
model = Model()
"""The model object that the GUI will work with.
@type: L{Model}
"""
config = ConfigParser.RawConfigParser()
"""Contains any configuration options that we want to keep track of on disk.

The configuration options are stored in C{BehaviourTool.ini}, and loaded up
when the program begins.
@type: RawConfigParser
"""

#class NonEmptyValidator(wx.PyValidator):
#    """This validator is used to ensure that the user has entered something
#    into the text object editor dialog's text field."""
#    def __init__(self):
#        """Standard constructor."""
#        wx.PyValidator.__init__(self)
#        self.Bind(wx.EVT_KILL_FOCUS, self.Validate)
#    
#    def Clone(self):
#        """ Standard cloner."""
#        return NonEmptyValidator()
#    
#    def Validate(self, window):
#        """Validate the contents of the given text control."""
#        textCtrl = self.GetWindow()
#        text = textCtrl.GetValue()
#        
#        if len(text) == 0:
#            textCtrl.SetBackgroundColour("pink")
#            #textCtrl.SetFocus()
#            textCtrl.Refresh()
#            return False
#        else:
#            textCtrl.SetBackgroundColour(wx.SystemSettings_GetColour(wx.SYS_COLOUR_WINDOW))
#            textCtrl.Refresh()
#            return True
#    
#    def TransferToWindow(self):
#        """Transfer data from validator to window.
#        
#        The default implementation returns False, indicating that an error
#        occurred.  We simply return True, as we don't do any data transfer."""
#        return True
#    
#    def TransferFromWindow(self):
#        """Transfer data from window to validator.
#        
#        The default implementation returns False, indicating that an error
#        occurred.  We simply return True, as we don't do any data transfer."""
#        return True

class BOptionsDialog(wx.Dialog):
    """BOptionsDialog is the dialog that we'll use to set various options in the config object."""
    def __init__(self, parent, id=wx.ID_ANY):
        """Create the widgets used in the dialog.
        @param parent: The object creating this dialog.
        @type parent: wx.Window
        @param id: An optional ID that can be passed to this dialog.
            There is no particular need to pass an id at this time.
        @type id: int
        """
        # Instead of calling wx.Dialog.__init__ we precreate the dialog
        # so we can set an extra style that must be set before
        # creation, and then we create the GUI object using the Create
        # method.
        pre = wx.PreDialog()
        #pre.SetExtraSytle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, id, title="Behaviour Tool Options", pos=wx.DefaultPosition,
                   size=wx.DefaultSize, style=wx.DEFAULT_DIALOG_STYLE)
        
        # This next step is the most important, it turns this Python
        # object into the real wrapper of the dialog (instead of pre)
        # as far as the wxPython extension is concerned.
        self.PostCreate(pre)
        
        # Path to util_verbs.nss (StaticText)
        util_verbs_st = wx.StaticText(self, wx.ID_ANY, "Path to util_verbs.nss")
        
        # Path to util_verbs.nss (TextCtrl)
        self.util_verbs_tc = wx.TextCtrl(self, wx.ID_ANY, "", size=(220, -1))
        """The TextControl containing the path to C{util_verbs.nss}.
        @type: wx.TextControl
        """
        
        # Browse for util_verbs.nss (Button)
        open_btn = wx.BitmapButton(self, wx.ID_OPEN, model.open_bmp)
        open_btn.SetToolTip(wx.ToolTip("Browse for the util_verbs.nss file"))
        open_btn.Bind(wx.EVT_BUTTON, self.OnBrowseUtilVerbs)
        
        # util_verbs sizer[Path util_verbs.nss <TextCtrl>]
        util_verbs_sizer = wx.BoxSizer(wx.HORIZONTAL)
        util_verbs_sizer.AddMany([(util_verbs_st, 0, wx.ALIGN_CENTER|wx.ALL, model.space),
                                  (self.util_verbs_tc, 1, wx.EXPAND|wx.ALL, model.space),
                                  (open_btn, 0, wx.ALL, model.space)])
        
        # Horizontal line
        line = wx.StaticLine(self, wx.ID_ANY, style=wx.LI_HORIZONTAL)
        
        # OK / Cancel buttons
        button_sizer = wx.StdDialogButtonSizer()
        
        # OK (Button)
        ok_btn = wx.Button(self, wx.ID_OK)
        ok_btn.SetDefault()
        button_sizer.AddButton(ok_btn)
        
        # Cancel (Button))
        cancel_btn = wx.Button(self, wx.ID_CANCEL)
        button_sizer.AddButton(cancel_btn)
        
        button_sizer.Realize()
        
        # Main sizer[util_verbs sizer, line, button sizer]
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([(util_verbs_sizer, 0, wx.ALL, model.space),
                       (line, 0, wx.EXPAND|wx.ALIGN_CENTER|wx.ALL, model.space),
                       (button_sizer, 0, wx.ALIGN_CENTER|wx.ALL, model.space)])
        
        self.__load()
        self.SetSizer(sizer)
        sizer.Fit(self)
    
    def __load(self):
        """Loads up the data from the config object."""
        if config.has_option("Options", "util_verbs_location"):
            self.util_verbs_tc.SetValue(config.get("Options", "util_verbs_location"))
    
    #{ Event handlers
    
    def OnBrowseUtilVerbs(self, event):
        """Open a FileDialog so the user can browse for the util_verbs.nss file.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        open_dlg = wx.FileDialog(self,
                                 message="Select the util_verbs.nss file",
                                 defaultDir=os.getcwd(),
                                 defaultFile="util_verbs.nss",
                                 style=wx.OPEN|wx.CHANGE_DIR)
        
        if open_dlg.ShowModal() == wx.ID_OK:
            self.util_verbs_tc.SetValue(open_dlg.GetPath())
        
        open_dlg.Destroy()
    
    #}
    
    def UpdateConfig(self):
        """Update the config object with the values in the widgets on the dialog."""
        
        util_verbs_path = self.util_verbs_tc.GetValue()
        if util_verbs_path != "":
            # Try loading up the util_verbs.nss file.  If it works, save the value.
            try:
                model.LoadUtilVerbs(util_verbs_path)
                config.set("Options", "util_verbs_location", util_verbs_path)
            except:
                fail_dlg = wx.MessageDialog(self,
                                            "Error loading the util_verbs.nss file.",
                                            "Error",
                                            wx.OK|wx.ICON_ERROR)
                fail_dlg.ShowModal()
                fail_dlg.Destroy()
                self.util_verbs_tc.SetValue("")
        else:
            config.set("Options", "util_verbs_location", util_verbs_path)

class ActorListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.TextEditMixin):
    """The ActorListCtrl is the widget that actors will be inputted into.
    
    It uses a few ListCtrl mixins to enable quick editing and aesthetics.
    It overloads SetStringItem to do validation and edit the model as changes are made."""
    def __init__(self, *args, **kwargs):
        """Initialize the Actor ListCtrl.
        @param args: Unnamed arguments, passed to the parent class's __init__ function.
        @param kwargs: Named arguments, passed to the parent class's __init__ function.
        """
        wx.ListCtrl.__init__(self, *args, **kwargs)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.TextEditMixin.__init__(self)
        
        self.InsertColumn(0, "Name")
        self.InsertColumn(1, "Description")
    
    def SetStringItem(self, index, col, data):
        """Do validation, then ensure the UI and engine stay in sync.
        @param index: The row index.
        @type index: int
        @param col: The column index.
        @type col: int
        @param data: The string to be set.
        @type data: string
        """
        # Validation: Make sure name is of the form o<uppercase>...
        #             Make sure the description is non-blank
        if col == 0:
            if data[0] != 'o':
                data = 'o' + data
            if data[1].islower():
                data = data[0] + data[1].upper() + data[2:]
            # Replace all spaces with underscores
            data = data.replace(' ', '_')
        
        else:
            if data == "":
                data = "Description"
        
        # Get the actor object.  This will be the (index+1)th element of the
        # nwvariables list that is an actor.
        count = 0
        ix = -1
        while count <= index:
            ix += 1
            if model.behaviour.nwvariables[ix].isActor == True:
                count += 1

        # Put the data into the actor object
        if col == 0:
            model.behaviour.nwvariables[ix].name = data
            model.UpdateNWVarNames()
        else:
            model.behaviour.nwvariables[ix].description = data
        
        wx.ListCtrl.SetStringItem(self, index, col, data)

class NWVarListCtrl(wx.ListCtrl, listmix.ListCtrlAutoWidthMixin, listmix.TextEditMixin):
    """The NWVarListCtrl is the widget that NWVariables will be inputted into.
    
    It uses a few ListCtrl mixins to enable quick editing and aesthetics.
    It overloads SetStringItem to do validation and edit the model as changes are made."""
    def __init__(self, *args, **kwargs):
        """Initialize the NWVariable ListCtrl.
        @param args: Unnamed arguments, passed to the parent class's __init__ function.
        @param kwargs: Named arguments, passed to the parent class's __init__ function.
        """
        wx.ListCtrl.__init__(self, *args, **kwargs)
        listmix.ListCtrlAutoWidthMixin.__init__(self)
        listmix.TextEditMixin.__init__(self)
        
        self.InsertColumn(0, "Type")
        self.InsertColumn(1, "Name")
        self.InsertColumn(2, "Description")
    
    def SetStringItem(self, index, col, data):
        """Do validation, then ensure the UI and engine stay in sync.
        @param index: The row index.
        @type index: int
        @param col: The column index.
        @type col: int
        @param data: The string to be set.
        @type data: string
        """
        # Validation: Make sure name is of the form o<uppercase>...
        #             Make sure the description is non-blank
        if col == 0:
            if data not in Codegen.valid_nwvar_types:
                data = Codegen.valid_nwvar_types[0]
        elif col == 1:
            # Prepend with the appropriate letter if it isn't already.
            type = self.GetItem(index, 0).GetText()
            if type[0] != data[0]:
                data = type[0] + data
            # Capitalize the second letter
            if data[1].islower():
                data = data[0] + data[1].upper() + data[2:]
            # Replace all spaces with underscores
            data = data.replace(' ', '_')
        else:
            # Make sure we get a non-empty description
            if data == "":
                data = "Description"
        
        # Get the nwvar object.  This will be the (index+1)th element of the
        # nwvariables list that is not an actor.
        count = 0
        ix = -1
        while count <= index:
            ix += 1
            if model.behaviour.nwvariables[ix].isActor == False:
                count += 1
        
        # Put the data into the actor object
        if col == 0:
            model.behaviour.nwvariables[ix].type = data
            model.UpdateNWVarNames()
        elif col ==1:
            model.behaviour.nwvariables[ix].name = data
            model.UpdateNWVarNames()
        else:
            model.behaviour.nwvariables[ix].description = data
        
        wx.ListCtrl.SetStringItem(self, index, col, data)

class VerbShapeHandler(ogl.ShapeEvtHandler):
    """Enables us to change tabs when a verb on the L{VerbCanvas} is double-clicked."""
    def __init__(self, notebook):
        """Sets up the instance variables.
        @param notebook: The notebook that contains the VerbCanvas.
        @type notebook: wx.NoteBook
        """
        ogl.ShapeEvtHandler.__init__(self)
        self.notebook = notebook
        """The notebook that contains the VerbCanvas.
        Keeping track of this object allows us to change the currently selected tab.
        @type: wx.NoteBook
        """
    
    #{ Event handlers
    
    def OnLeftDoubleClick(self, *dontcare):
        """Changes the currently selected tab to the one corresponding to the shape
        that was double-clicked.
        @param dontcare: The unnamed arguments; they are ignored.
        """
        shape = self.GetShape()
        canvas = shape.GetCanvas()
        ix = canvas.shapes.index(shape)
        self.notebook.SetSelection(ix+1)
    
    #}

class VerbCanvas(ogl.ShapeCanvas):
    """The canvas that the verb graph will be drawn on.  Uses the OGL library."""
    def __init__(self, parent, *args, **kwargs):
        """Sets up the instance variables, widgets, and widget settings.
        @param parent: The object creating this widget.
        @type parent: wx.Window
        @param args: Unnamed arguments, passed to the parent class's __init__ function.
        @param kwargs: Named arguments, passed to the parent class's __init__ function.
        """
        
        ogl.ShapeCanvas.__init__(self, parent, *args, **kwargs)
        
        self.SetBackgroundColour(wx.WHITE)
        self.diagram = ogl.Diagram()
        """The diagram associated with the canvas.  All canvases require a diagram.
        @type: ogl.Diagram
        """
        self.SetDiagram(self.diagram)
        self.diagram.SetCanvas(self)
        self.shapes = []
        """The shapes currently shown on the canvas.
        @type: list of ogl.Shape objects
        """
    
    def ClearShapes(self):
        """Remove all the shapes currently on the canvas."""
        self.shapes = []
        self.diagram.DeleteAllShapes()
    
    def DrawShapes(self):
        """Iterate through the verbs in the model's behaviour, drawing a shape for each.
        Draw a line for each follower connection."""
        # Each verb should be the same height
        height = 30.0
        # We'll arrange the verbs in columns...
        columns = 2
        # The spacing will determine how spread apart the shapes are
        spacing = 20.0
        # We'll determine our X offset based on the size of the canvas
        size = self.GetSizeTuple()
        x_offset = (size[0] / columns) - spacing*3
        # Our Y offset is based on the height of a verb
        y_offset = height + spacing
        
        # Draw the verb shapes
        for ix, verb in enumerate(model.behaviour.verbs):
            width = len(verb.context_name) * 7.6 + 8.0
            shape = ogl.RectangleShape(width, height)
            
            # Determine the X and Y positions from the offset and ix
            shape.SetX((x_offset * (ix%columns)) + (spacing*3))
            shape.SetY((y_offset * (ix/columns)) + spacing)
            
            if verb.terminal is True:
                shape.SetPen(wx.Pen(wx.BLACK, 2))
                shape.SetBrush(wx.LIGHT_GREY_BRUSH)
                shape.SetCornerRadius(0)
            else:
                shape.SetPen(wx.Pen(wx.BLACK, 2))
                shape.SetCornerRadius(6)
            
            shape.SetFont(model.shape_font)
            shape.AddText(verb.context_name)
            shape.SetCanvas(self)
            shape.SetId(ix)
            
            panel = self.GetParent()
            evthandler = VerbShapeHandler(panel.GetGrandParent())
            evthandler.SetShape(shape)
            evthandler.SetPreviousHandler(shape.GetEventHandler())
            shape.SetEventHandler(evthandler)
            
            self.shapes.append(shape)
            self.AddShape(shape)
        
        # Draw the lines to connect the verbs
        for ix, verb in enumerate(model.behaviour.verbs):
            for follower in verb.followers:
                line = ogl.LineShape()
                line.SetCanvas(self)
                line.SetPen(wx.BLACK_PEN)
                line.SetBrush(wx.BLACK_BRUSH)
                line.AddArrow(ogl.ARROW_ARROW)
                line.MakeLineControlPoints(2)
                self.shapes[ix].AddLine(line, self.shapes[model.behaviour.verbs.index(follower)])
                self.diagram.AddShape(line)
                line.Show(True)
        
        self.diagram.ShowAll(1)
    
    def ClearAndDrawShapes(self):
        """Remove then draw all the shapes on the canvas."""
        self.ClearShapes()
        self.DrawShapes()

class NWScriptSTC(wx.stc.StyledTextCtrl):
    """A styled text control (a wxWidget based on Scintilla) for the display of NWScript code.
    This could also be ideal for editing NWScript. (This program only uses is to display code, however)
    A lot of the code was swiped from the wxPython demo, with changes to make it fit NWScript."""
    def __init__(self, parent, id=wx.ID_ANY):
        """Sets up the lexer, style, and other elements of the STC.
        @param parent: The object creating this widget.
        @type parent: wx.Window
        @param id: An optional ID that can be passed to this widget.
            There is no particular need to pass an id at this time.
        @type id: int
        """
        wx.stc.StyledTextCtrl.__init__(self, parent, id, wx.DefaultPosition, wx.DefaultSize)

        # NWScript keyword list to enable syntax highlighting on the code preview.
        nwscript_keywords = ("const int object string void if return"
                             " TRUE FALSE for while switch case break continue")
        
        # Use the CPP lexer, as it's closest to NWScript
        self.SetLexer(wx.stc.STC_LEX_CPP)
        self.SetKeyWords(0, nwscript_keywords)
        
        # Enable folding
        self.SetProperty("fold", "1")
        self.SetProperty("fold.comment","1")
        self.SetProperty("fold.compact","1")
        
        # Set up margins
        self.SetMargins(2,2)
        
        # Left margin - Line #'s
        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        # Reasonable value for 3 digits using a mono font (24 pix)
        # Generated scripts would need hundreds of verbs to reach 100 lines.
        self.SetMarginWidth(1, 24)
        
        # Right margin - Fold markers
        self.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)
        # and now set up the fold markers
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND,     wx.stc.STC_MARK_BOXPLUSCONNECTED,  "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID, wx.stc.STC_MARK_BOXMINUSCONNECTED, "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL, wx.stc.STC_MARK_TCORNER,  "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL,    wx.stc.STC_MARK_LCORNER,  "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB,     wx.stc.STC_MARK_VLINE,    "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER,        wx.stc.STC_MARK_BOXPLUS,  "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN,    wx.stc.STC_MARK_BOXMINUS, "white", "black")
        
        # Indentation and tab stuff
        self.SetIndent(4)               # NWScript uses 4 character tabs
        self.SetIndentationGuides(True) # Show indent guides
        self.SetBackSpaceUnIndents(True)# Backspace unindents rather than delete 1 space
        self.SetTabIndents(True)        # Tab key indents
        self.SetTabWidth(4)             # Proscribed tab size for wx
        self.SetUseTabs(False)          # Use spaces rather than tabs
        
        # The Aurora editor uses this edge mode as well.
        self.SetEdgeMode(wx.stc.STC_EDGE_LINE)
        self.SetEdgeColumn(80)
        
        # White space
        self.SetViewWhiteSpace(False)   # Don't view white space
        
        # EOL: Since we are loading/saving ourselves, and the
        # strings will always have \n's in them, set the STC to
        # edit them that way.            
        self.SetEOLMode(wx.stc.STC_EOL_CRLF)
        self.SetViewEOL(False)
        
        # Global default style
        if wx.Platform == '__WXMSW__':
            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, 
                              'fore:#000000,back:#FFFFFF,face:Courier New,size:9')
        elif wx.Platform == '__WXMAC__':
            # TODO: if this looks fine on Linux too, remove the Mac-specific case 
            # and use this whenever OS != MSW.
            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, 
                              'fore:#000000,back:#FFFFFF,face:Courier')
        else:
            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT, 
                              'fore:#000000,back:#FFFFFF,face:Courier,size:9')

        # Clear styles and revert to default.
        self.StyleClearAll()

        # Following style specs only indicate differences from default.
        # The rest remains unchanged.

        # Line numbers in margin
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,'fore:#000000,back:#99A9C2')    
        # Highlighted brace
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,'fore:#00009D,back:#FFFF00')
        # Unmatched brace
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,'fore:#00009D,back:#FF0000')
        # Indentation guide
        self.StyleSetSpec(wx.stc.STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")

        # Python styles
        self.StyleSetSpec(wx.stc.STC_P_DEFAULT, 'fore:#000000')
        # Comments
        self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE,  'fore:#008000,back:#F0FFF0')
        self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK, 'fore:#008000,back:#F0FFF0')
        # Numbers
        self.StyleSetSpec(wx.stc.STC_P_NUMBER, 'fore:#008080')
        # Strings and characters
        self.StyleSetSpec(wx.stc.STC_P_STRING, 'fore:#800080')
        self.StyleSetSpec(wx.stc.STC_P_CHARACTER, 'fore:#800080')
        # Keywords
        self.StyleSetSpec(wx.stc.STC_P_WORD, 'fore:#000080,bold')
        # Class names
        self.StyleSetSpec(wx.stc.STC_P_CLASSNAME, 'fore:#0000FF,bold')
        # Function names
        self.StyleSetSpec(wx.stc.STC_P_DEFNAME, 'fore:#008080,bold')
        # Operators
        self.StyleSetSpec(wx.stc.STC_P_OPERATOR, 'fore:#800000')
        # Identifiers. I leave this as not bold because everything seems
        # to be an identifier if it doesn't match the above criterae
        self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, 'fore:#000000')

        # Caret color
        self.SetCaretForeground("BLUE")
        # Selection background
        self.SetSelBackground(1, '#66CCFF')

        self.SetSelBackground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True, wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))
        
        # Bind the marginclick event to enable folding and unfolding
        self.Bind(wx.stc.EVT_STC_MARGINCLICK, self.OnMarginClick)
    
    #{ Event handlers
    
    def OnMarginClick(self, event):
        """Fold and unfold as needed.
        @param event: Event created by EVT_STC_MARGINCLICK.
        @type event: wx.CommandEvent
        """
        if event.GetMargin() == 2:
            lineClicked = self.LineFromPosition(event.GetPosition())
            self.ToggleFold(lineClicked)
    
    #}

class BehaviourCodePreviewPanel(wx.Panel):
    """A panel containing widgets to select between two choices of viewable code,
    and preview it."""
    def __init__(self, parent, *args, **kwargs):
        """Sets up the instance variables, widgets, and widget settings.
        @param parent: The object creating this widget.
        @type parent: wx.Window
        @param args: Unnamed arguments, passed to the parent class's __init__ function.
        @param kwargs: Named arguments, passed to the parent class's __init__ function.
        """
        wx.Panel.__init__(self, parent, wx.ID_ANY, *args, **kwargs)
        
        # Preview Generated Code (StaticText)
        preview_st = wx.StaticText(self, wx.ID_ANY, "Preview Generated Code")
        preview_st.SetFont(model.title_font)
        
        # <b_ or z_b_ file Choice>
        self.file_ch = wx.Choice(self, wx.ID_ANY)
        """The dropdown box containing the choice of which script file to preview.
        @type: wx.Choice
        """
        self.Bind(wx.EVT_CHOICE, self.OnChoice, self.file_ch)
        
        # Refresh (Button)
        refresh_btn = wx.BitmapButton(self, wx.ID_REFRESH, model.refresh_bmp)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, refresh_btn)
        refresh_btn.SetToolTip(wx.ToolTip("Refresh the generated code preview"))
        
        # Preview sizer[Preview Generated Code  <choice> <refresh>]
        preview_sizer = wx.BoxSizer(wx.HORIZONTAL)
        preview_sizer.AddMany([(preview_st, 0, wx.ALL, model.space),
                               ((0,0), 0, wx.ALL, model.space),
                               (self.file_ch, 0, wx.ALL, model.space),
                               (refresh_btn, 0, wx.ALL, model.space)])

        # Code Preview StyledTextCtrl
        self.stc = NWScriptSTC(self, wx.ID_ANY)
        """The styled text control used to display the generated code.
        @type: L{NWScriptSTC}
        """
        self.stc.SetReadOnly(True)

        # Main sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.AddMany([(preview_sizer, 0, wx.ALL, model.space),
                       (self.stc, 1, wx.EXPAND|wx.ALL, model.space)])
        
        self.__load()
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
    
    def __load(self):
        """Load data from the model to populate the widgets."""
        b_name = model.behaviour.name.lower()
        
        self.file_ch.SetItems(["b_%s" % b_name, "z_b_%s" % b_name])
    
    #{ Event handlers
    
    def OnChoice(self, event):
        """Refresh the STC upon selecting which script file to preview.
        @param event: Event created by EVT_CHOICE.
        @type event: wx.CommandEvent
        """
        self.RefreshSTC(event.GetSelection())
    
    def OnRefresh(self, event):
        """Refresh the STC upon clicking the refresh button.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        self.RefreshSTC(self.file_ch.GetCurrentSelection())
    
    #}
    
    def RefreshSTC(self, selection):
        """Load text into the STC.  The text depends on the selection parameter.
        @param selection: Which code should be previewed, the C{b_<Behaviour>}
            code or C{z_b_<Behaviour>} code?
        @type selection: int
        """
        # 0 is the b_ file, 1 is the z_b_ file
        if selection == 0:
            self.stc.SetReadOnly(False)
            self.stc.SetText(model.behaviour.GenerateBCode())
            self.stc.SetReadOnly(True)
        else:
            self.stc.SetReadOnly(False)
            self.stc.SetText(model.behaviour.GenerateZBCode())
            self.stc.SetReadOnly(True)
    
    def UpdateChoice(self):
        """Update the file_ch dropdown box to reflect the new behaviour name.
        This should be called whenever the behaviour names changes."""
        b_name = model.behaviour.name.lower()
        select = self.file_ch.GetCurrentSelection()
        self.file_ch.SetString(0, "b_%s" % b_name)
        self.file_ch.SetString(1, "z_b_%s" % b_name)
        self.file_ch.SetSelection(select)
    
    def UpdateState(self):
        """Refresh the STC."""
        self.RefreshSTC(self.file_ch.GetCurrentSelection())

class VerbCodePreviewPanel(wx.Panel):
    """A panel containing widgets to view two code preview widgets simultaneously."""
    def __init__(self, parent, verb, *args, **kwargs):
        """Sets up the instance variables, widgets, and widget settings.
        @param parent: The object creating this widget.
        @type parent: wx.Window
        @param verb: The verb whose generated code this panel is previewing.
        @type verb: L{Verb}
        @param args: Unnamed arguments, passed to the parent class's __init__ function.
        @param kwargs: Named arguments, passed to the parent class's __init__ function.
        """
        wx.Panel.__init__(self, parent, wx.ID_ANY, *args, **kwargs)
        
        # Keep track of the verb we're working on.
        self.verb = verb
        """The verb whose generated code this panel is previewing.
        @type: L{Verb}
        """
        
        # Constants
        self.__CONTROL = 1
        """Constant to pass to L{VerbCodePreviewPanel.RefreshSTC} when we wish
        to refresh the control STC.
        @type: int
        """
        self.__CHECKCUES = 2
        """Constant to pass to L{VerbCodePreviewPanel.RefreshSTC} when we wish
        to refresh the checkcues STC.
        @type: int
        """
        self.__BOTH = 4
        """Constant to pass to L{VerbCodePreviewPanel.RefreshSTC} when we wish
        to refresh both STCs.
        @type: int
        """
        
        # Control Preview (StaticText)
        control_st = wx.StaticText(self, wx.ID_ANY, "Control Preview")
        control_st.SetFont(model.title_font)

        # Refresh (Button)
        refresh_control_btn = wx.BitmapButton(self, wx.ID_REFRESH, model.refresh_bmp)
        refresh_control_btn.Bind(wx.EVT_BUTTON, self.OnRefreshControl)
        refresh_control_btn.SetToolTip(wx.ToolTip("Refresh the generated code preview"))
        
        # Control sizer[Control Preview  <Refresh button>]
        control_sizer = wx.BoxSizer(wx.HORIZONTAL)
        control_sizer.AddMany([(control_st, 0, wx.ALL, model.space),
                               ((0,0), 0, wx.ALL, model.space),
                               (refresh_control_btn, 0, wx.ALL, model.space)])

        # Control StyledTextCtrl
        self.control_stc = NWScriptSTC(self, wx.ID_ANY)
        """The styled text control used to display the control code.
        @type: L{NWScriptSTC}
        """
        self.control_stc.SetReadOnly(True)
        
        # Left sizer [Preview sizer, Control STC]
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.AddMany([(control_sizer, 0, wx.ALL, model.space),
                            (self.control_stc, 1, wx.EXPAND|wx.ALL, model.space)])
        
        # Checkcues Preview (StaticText)
        checkcues_st = wx.StaticText(self, wx.ID_ANY, "Checkcues Preview")
        checkcues_st.SetFont(model.title_font)

        # Refresh (Button)
        refresh_checkcues_btn = wx.BitmapButton(self, wx.ID_REFRESH, model.refresh_bmp)
        refresh_checkcues_btn.Bind(wx.EVT_BUTTON, self.OnRefreshCheckcues)
        refresh_checkcues_btn.SetToolTip(wx.ToolTip("Refresh the generated code preview"))
        
        # Checkcues sizer[Preview Control Code  <Refresh button>]
        checkcues_sizer = wx.BoxSizer(wx.HORIZONTAL)
        checkcues_sizer.AddMany([(checkcues_st, 0, wx.ALL, model.space),
                                 ((0,0), 0, wx.ALL, model.space),
                                 (refresh_checkcues_btn, 0, wx.ALL, model.space)])

        # Control StyledTextCtrl
        self.checkcues_stc = NWScriptSTC(self, wx.ID_ANY)
        """The styled text control used to display the checkcues code.
        @type: L{NWScriptSTC}
        """
        self.checkcues_stc.SetReadOnly(True)        
        
        # Right sizer [Checkcues sizer, Checkcues STC]
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.AddMany([(checkcues_sizer, 0, wx.ALL, model.space),
                             (self.checkcues_stc, 1, wx.EXPAND|wx.ALL, model.space)])    
        
        # Main sizer [Left sizer, Right sizer]
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddMany([(left_sizer, 1, wx.EXPAND),
                       (right_sizer, 1, wx.EXPAND)])
 
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
    
    #{ Event handlers
    
    def OnRefreshControl(self, event):
        """Refresh the control STC.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        self.RefreshSTC(self.__CONTROL)
    
    def OnRefreshCheckcues(self, event):
        """Refresh the checkcues STC.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        self.RefreshSTC(self.__CHECKCUES)
    
    #}
    
    def RefreshSTC(self, which):
        """Refresh one or both of the code preview STC's.
        @param which: Which STC(s) should be refreshed?
        @type which: int
        """
        if which is self.__CONTROL or which is self.__BOTH:
            self.control_stc.SetReadOnly(False)
            self.control_stc.SetText(self.verb.GenerateControlCode())
            self.control_stc.SetReadOnly(True)            
        
        if which is self.__CHECKCUES or which is self.__BOTH:
            self.checkcues_stc.SetReadOnly(False)
            self.checkcues_stc.SetText(self.verb.GenerateCheckcuesCode())
            self.checkcues_stc.SetReadOnly(True)
    
    def UpdateState(self):
        """Refresh both STC's."""
        self.RefreshSTC(self.__BOTH)

class BehaviourPanel(wx.Panel):
    """This panel contains widgets to display and modify behaviour-wide information."""
    def __init__(self, parent, *args, **kwargs):
        """Sets up the instance variables, widgets, and widget settings.
        @param parent: The object creating this widget.
        @type parent: wx.Window
        @param args: Unnamed arguments, passed to the parent class's __init__ function.
        @param kwargs: Named arguments, passed to the parent class's __init__ function.
        """
        wx.Panel.__init__(self, parent, wx.ID_ANY, *args, **kwargs)
        
        # Set up the lists we need
        self.actor_trash = []
        """Actors removed from the L{ActorListCtrl} are put in this list for later retrieval.
        @type: list of (string, string) tuples
        """
        self.nwvar_trash = []
        """NWVariables removed from the L{NWVarListCtrl} are put in this list for later retrieval.
        @type: list of (string, string, string) tuples
        """
        self.verb_trash = []
        """Verbs removed from the behaviour are put in this list for later retrieval.
        @type: list of L{Verb}s
        """
        
        # Behaviour name (StaticText)
        b_name_st = wx.StaticText(self, wx.ID_ANY, "Behaviour name")
        
        # Behaviour name (TextCtrl)
        self.b_name_tc = wx.TextCtrl(self, wx.ID_ANY, model.behaviour.name)
        """The text field containing the name of the behaviour.
        @type: wx.TextCtrl
        """
        self.b_name_tc.Bind(wx.EVT_KILL_FOCUS, self.OnNameKillFocus)
        
        # Behaviour sizer[Behaviour name: <TextCtrl>]
        b_name_sizer = wx.BoxSizer(wx.HORIZONTAL)
        b_name_sizer.AddMany([(b_name_st, 0, wx.ALL, model.space),
                              (self.b_name_tc, 1)])

        # Actors (StaticText)
        actors_st = wx.StaticText(self, wx.ID_ANY, "Actors")
        actors_st.SetFont(model.title_font)
        
        # AddActor (Button)
        add_actor_btn = wx.BitmapButton(self, wx.ID_ADD, model.add_bmp)
        add_actor_btn.SetToolTip(wx.ToolTip("Add a new actor"))
        add_actor_btn.Bind(wx.EVT_BUTTON, self.OnAddActor)
        
        # DeleteActor (Button)
        del_actor_btn = wx.BitmapButton(self, wx.ID_DELETE, model.del_bmp)
        del_actor_btn.SetToolTip(wx.ToolTip("Delete the selected actor"))
        del_actor_btn.Bind(wx.EVT_BUTTON, self.OnDelActor)
        
        # TrashActor (Button)
        trash_actor_btn = wx.BitmapButton(self, wx.ID_UNDELETE, model.trash_bmp)
        trash_actor_btn.SetToolTip(wx.ToolTip("Restore a deleted actor"))
        trash_actor_btn.Bind(wx.EVT_BUTTON, self.OnActorTrash)
        
        # Actor sizer[Actors <Add Button><Del Button><Trash Button>]
        actors_sizer = wx.BoxSizer(wx.HORIZONTAL)
        actors_sizer.AddMany([(actors_st, 0, wx.ALL, model.space),
                              ((0,0), 1),
                              (add_actor_btn, 0),
                              (del_actor_btn, 0),
                              (trash_actor_btn, 0)])
        
        # Actors ListCtrl
        self.actors_lc = ActorListCtrl(self, wx.ID_ANY,
                                       style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        """The editable list of actors involved in the behaviour.
        @type: L{ActorListCtrl}
        """
        
        # Other Variables (StaticText)
        nwvars_st = wx.StaticText(self, wx.ID_ANY, "Other Variables")
        nwvars_st.SetFont(model.title_font)
        
        # AddNWVar (Button)
        add_nwvar_btn = wx.BitmapButton(self, wx.ID_ADD, model.add_bmp)
        add_nwvar_btn.SetToolTip(wx.ToolTip("Add a new variable"))
        add_nwvar_btn.Bind(wx.EVT_BUTTON, self.OnAddNWVar)
        
        # DelNWVar (Button)
        del_nwvar_btn = wx.BitmapButton(self, wx.ID_DELETE, model.del_bmp)
        del_nwvar_btn.SetToolTip(wx.ToolTip("Delete the selected variable"))
        del_nwvar_btn.Bind(wx.EVT_BUTTON, self.OnDelNWVar)
        
        # TrashNWVar (Button)
        trash_nwvar_btn = wx.BitmapButton(self, wx.ID_UNDELETE, model.trash_bmp)
        trash_nwvar_btn.SetToolTip(wx.ToolTip("Restore a deleted variable"))
        trash_nwvar_btn.Bind(wx.EVT_BUTTON, self.OnNWVarTrash)
        
        # NWVars sizer[Other Variables <Add Button><Del Button><Trash Button>]
        nwvars_sizer = wx.BoxSizer(wx.HORIZONTAL)
        nwvars_sizer.AddMany([(nwvars_st, 0, wx.ALL, model.space),
                              ((0,0), 1),
                              (add_nwvar_btn, 0),
                              (del_nwvar_btn, 0),
                              (trash_nwvar_btn, 0)])

        # NWVars ListCtrl
        self.nwvars_lc = NWVarListCtrl(self, wx.ID_ANY,
                                       style=wx.LC_REPORT|wx.LC_SINGLE_SEL)
        """The editable list of variables involved in the behaviour.
        @type: L{NWVarListCtrl}
        """
        
        # Left sizer[Name sizer, Actor sizer, Actor ListCtrl, NWVar sizer, NWVar ListCtrl]
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.AddMany([(b_name_sizer, 0, wx.EXPAND|wx.ALL, model.space),
                            (actors_sizer, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, model.space),
                            (self.actors_lc, 1, wx.EXPAND|wx.ALL, model.space),
                            (nwvars_sizer, 0, wx.EXPAND|wx.TOP|wx.LEFT|wx.RIGHT, model.space),
                            (self.nwvars_lc, 1, wx.EXPAND|wx.ALL, model.space)])
        
        # Verbs (StaticText)
        verb_st = wx.StaticText(self, wx.ID_ANY, "Verbs")
        verb_st.SetFont(model.title_font)

        # AddVerb (Button)
        add_verb_btn = wx.BitmapButton(self, wx.ID_ADD, model.add_bmp)
        add_verb_btn.SetToolTip(wx.ToolTip("Add a new verb"))
        add_verb_btn.Bind(wx.EVT_BUTTON, self.OnAddVerb)
        
        # TrashVerb (Button)
        trash_verb_btn = wx.BitmapButton(self, wx.ID_UNDELETE, model.trash_bmp)
        trash_verb_btn.SetToolTip(wx.ToolTip("Restore a deleted verb"))
        trash_verb_btn.Bind(wx.EVT_BUTTON, self.OnVerbTrash)  
        
        # Verb sizer[Verbs <Add Button><Del Button><Trash Button>]
        verbs_sizer = wx.BoxSizer(wx.HORIZONTAL)
        verbs_sizer.AddMany([(verb_st, 0, wx.ALL, model.space),
                             ((0,0), 1),
                             (add_verb_btn, 0),
                             (trash_verb_btn, 0)])
        
        # OGL object
        self.ogl_canvas = VerbCanvas(self)
        """The generated diagram showing the relationship between the verbs in the behaviour.
        @type: L{VerbCanvas}
        """
        
        # Right sizer[Verb sizer, OGL object]
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.AddMany([(verbs_sizer, 0, wx.EXPAND|wx.ALL, model.space),
                             (self.ogl_canvas, 1, wx.EXPAND|wx.ALL, model.space)])
        
        # Main sizer[Left sizer, Right sizer]
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddMany([(left_sizer, 1, wx.EXPAND|wx.ALL, model.space),
                       (right_sizer, 1, wx.EXPAND|wx.ALL, model.space)])
        
        # Fill in information from the model
        self.__load()
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
    
    def __load(self):
        """Load information from the model to populate our widgets."""
        
        # Behaviour name
        self.b_name_tc.SetValue(model.behaviour.name)
        
        # NWVariables
        for nwvar in model.behaviour.nwvariables:
            if nwvar.isActor == True:
                self.AddActorToList(nwvar.name, nwvar.description)
            else:
                self.AddNWVarToList(nwvar.type, nwvar.name, nwvar.description)
        
        # OGL
        self.ogl_canvas.DrawShapes()
    
    #{ Event handlers
    
    def OnAddActor(self, event):
        """Since we don't need the event object, just call L{AddActor}.
        @param event: Event created by EVT_BUTTON.  Not used.
        @type event: wx.CommandEvent
        """
        self.AddActor("oName", "Description")
    
    def OnDelActor(self, event):
        """Move the currently selected ListItem to the trash.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        selected_ix = self.actors_lc.GetFirstSelected()
        
        if selected_ix != -1:
            # Get the actor object.  This will be the (selected_ix+1)th element 
            # of the nwvariables list that is an actor.
            count = 0
            ix = -1
            while count <= selected_ix:
                ix += 1
                if model.behaviour.nwvariables[ix].isActor == True:
                    count += 1
            
            del model.behaviour.nwvariables[ix]
            model.UpdateNWVarNames()
            selected_item = (self.actors_lc.GetItem(selected_ix, 0).GetText(),
                             self.actors_lc.GetItem(selected_ix, 1).GetText())
            self.actor_trash.append(selected_item)
            self.actors_lc.DeleteItem(selected_ix)
    
    def OnActorTrash(self, event):
        """Show a popup menu with the previously deleted actors.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        actor_menu = wx.Menu()
        
        actor_menu.Append(-1, "Deleted Actors")
        actor_menu.AppendSeparator()
        
        for ix, actor in enumerate(self.actor_trash):
            if len(actor[1]) > model.desc_length:
                desc = actor[1][:model.desc_length-3] + "..."
            else:
                desc = actor[1]
            actor_menu.Append(ix, "%s - %s" % (actor[0], desc))
            actor_menu.Bind(wx.EVT_MENU, self.OnRestoreActor, id=ix)
        
        self.PopupMenu(actor_menu)
    
    def OnRestoreActor(self, event):
        """Restore a previously deleted actor.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        ix = event.GetId()
        actor = self.actor_trash.pop(ix)
        
        if actor != None:
            self.AddActor(actor[0], actor[1])
    
    def OnAddNWVar(self, event):
        """Since we don't need the event object, just call L{AddNWVar}.
        @param event: Event created by EVT_BUTTON. Not used.
        @type event: wx.CommandEvent
        """
        self.AddNWVar("object", "oName", "Description")
    
    def OnDelNWVar(self, event):
        """Move the currently selected ListItem to the trash.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        selected_ix = self.nwvars_lc.GetFirstSelected()
        
        if selected_ix != -1:
            # Get the nwvar object.  This will be the (selected_ix+1)th element 
            # of the nwvariables list that is not an actor.
            count = 0
            ix = -1
            while count <= selected_ix:
                ix += 1
                if model.behaviour.nwvariables[ix].isActor == False:
                    count += 1

            del model.behaviour.nwvariables[ix]
            model.UpdateNWVarNames()    
            selected_item = (self.nwvars_lc.GetItem(selected_ix, 0).GetText(),
                             self.nwvars_lc.GetItem(selected_ix, 1).GetText(),
                             self.nwvars_lc.GetItem(selected_ix, 2).GetText())
            self.nwvar_trash.append(selected_item)
            self.nwvars_lc.DeleteItem(selected_ix)
    
    def OnNWVarTrash(self, event):
        """Show a popup menu with the previously deleted variables.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        nwvar_menu = wx.Menu()
        
        nwvar_menu.Append(-1, "Deleted Variables")
        nwvar_menu.AppendSeparator()
        
        for ix, nwvar in enumerate(self.nwvar_trash):
            if len(nwvar[2]) > model.desc_length:
                desc = nwvar[2][:model.desc_length-3] + "..."
            else:
                desc = nwvar[2]            
            nwvar_menu.Append(ix, "%s %s - %s" % (nwvar[0], nwvar[1], desc))
            nwvar_menu.Bind(wx.EVT_MENU, self.OnRestoreNWVar, id=ix)

        self.PopupMenu(nwvar_menu)
    
    def OnRestoreNWVar(self, event):
        """Restore a previously deleted nwvar.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        ix = event.GetId()
        nwvar = self.nwvar_trash.pop(ix)
        
        if nwvar != None:
            self.AddNWVar(nwvar[0], nwvar[1], nwvar[2])
    
    def OnAddVerb(self, event):
        """Create a verb and add a tab to the main NoteBook.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        newverb = Codegen.Verb(model.behaviour)
        newverb.context_name = "New_Verb"
        model.behaviour.verbs.append(newverb)
        model.UpdateVerbNames()
        
        self.AddVerbPage(newverb)
    
    def OnVerbTrash(self, event):
        """Show a popup menu with the previously deleted verbs.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        verb_menu = wx.Menu()

        verb_menu.Append(-1, "Deleted Verbs")
        verb_menu.AppendSeparator()
        
        for ix, verb in enumerate(self.verb_trash):
            if verb.actual_name != "":
                verb_menu.Append(ix, "%s (%s)" % (verb.context_name, verb.actual_name))
            else:
                verb_menu.Append(ix, verb.context_name)
            verb_menu.Bind(wx.EVT_MENU, self.OnRestoreVerb, id=ix)
        
        self.PopupMenu(verb_menu)
    
    def OnRestoreVerb(self, event):
        """Restore a previously deleted verb.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        ix = event.GetId()
        verb = self.verb_trash.pop(ix)
        
        if verb != None:
            self.AddVerb(verb)
    
    def OnNameKillFocus(self, event):
        """Change the model's behaviour name and update the UI to reflect the change.
        @param event: Event created by EVT_KILL_FOCUS.
        @type event: wx.CommandEvent
        """
        name = self.b_name_tc.GetValue()
        name = name[:11]
        name = name.replace(' ', '_')
        self.b_name_tc.SetValue(name)
        model.behaviour.name = name
        
        # Change the text on the tab
        notebook = self.GetGrandParent()
        notebook.SetPageText(notebook.GetSelection(), name)        

        # Update the Choice on the BehaviourCodePreviewPanel
        splitter = self.GetParent()
        splitter.bottom.UpdateChoice()
    
    #}
    
    def AddActor(self, name, desc):
        """Create a new actor and add it to the ActorListCtrl.
        @param name: Name of the actor.
        @type name: string
        @param desc: Description of the actor.
        @type desc: string
        """
        model.behaviour.nwvariables.append(Codegen.NWVariable(type="object",
                                                              name=name,
                                                              description=desc,
                                                              isActor = True))
        model.UpdateNWVarNames()        
        self.AddActorToList(name, desc)
    
    def AddActorToList(self, name, desc):
        """Add an actor to the ListCtrl.
        @param name: Name of the actor.
        @type name: string
        @param desc: Description of the actor.
        @type desc: string
        """
        self.actors_lc.Append((name, desc))
    
    def AddNWVar(self, type, name, desc):
        """Create a new nwvar and add it to the NWVarListCtrl.
        @param type: Type of the NWVar.
        @type type: string
        @param name: Name of the NWVar.
        @type name: string
        @param desc: Description of the NWVar.
        @type desc: string
        """
        model.behaviour.nwvariables.append(Codegen.NWVariable(type=type,
                                                              name=name,
                                                              description=desc,
                                                              isActor = False))
        model.UpdateNWVarNames()
        self.AddNWVarToList(type, name, desc)
    
    def AddNWVarToList(self, type, name, desc):
        """Add an NWVar to the NWVarListCtrl.
        @param type: Type of the NWVar.
        @type type: string
        @param name: Name of the NWVar.
        @type name: string
        @param desc: Description of the NWVar.
        @type desc: string
        """
        self.nwvars_lc.Append((type, name, desc))
    
    def AddVerb(self, verb):
        """Add the specified verb to the model and notebook.
        @param verb: The verb to be added to the model and notebook.
        @type verb: L{Verb}
        """
        model.behaviour.verbs.append(verb)
        model.UpdateVerbNames()
        self.AddVerbPage(verb)
    
    def AddVerbPage(self, verb):
        """Add a tab to the main notebook containing a verb panel.
        @param verb: The verb to be edited in the verb panel.
        @type verb: L{Verb}
        """
        notebook = self.GetGrandParent()
        v_splitter = VerbSplitter(notebook, verb)
        notebook.AddPage(v_splitter, verb.context_name)
        notebook.SetSelection(notebook.GetPageCount()-1)
    
    def UpdateState(self):
        """Redraw the verb diagram."""
        self.ogl_canvas.ClearAndDrawShapes()

class VerbPanel(wx.Panel):
    """This panel contains widgets to view and modify a verb."""
    def __init__(self, parent, verb, *args, **kwargs):
        """Sets up the instance variables, widgets, and widget settings.
        @param parent: The object creating this widget.
        @type parent: wx.Window
        @param verb: The verb this panel is displaying.
        @type verb: L{Verb}
        @param args: Unnamed arguments, passed to the parent class's __init__ function.
        @param kwargs: Named arguments, passed to the parent class's __init__ function.
        """
        wx.Panel.__init__(self, parent, wx.ID_ANY, *args, **kwargs)
        
        # Get the verb this panel will work on.
        self.verb = verb
        """The verb this panel is displaying.
        @type verb: L{Verb}
        """
        
        # Set up our trashes
        self.precond_trash = []
        """Preconditions removed from the verb are put in this list for later retrieval.
        @type: list of strings
        """
        self.follower_trash = []
        """Followers removed from the verb are put in this list for later retrieval.
        @type: list of ints
        """
        
        # Set up the lists we'll use to keep track of the comboboxes and choices we add.
        self.object_cbs = []
        """Keeps track of the ItemContainer objects that contain lists of NWVariables of type 'object'.
        @type: list of wx.ItemContainer objects
        """
        self.string_cbs = []
        """Keeps track of the ItemContainer objects that contain lists of NWVariables of type 'string'.
        @type: list of wx.ItemContainer objects
        """
        self.int_cbs = []
        """Keeps track of the ItemContainer objects that contain lists of NWVariables of type 'int'.
        @type: list of wx.ItemContainer objects
        """
        self.float_cbs = []
        """Keeps track of the ItemContainer objects that contain lists of NWVariables of type 'float'.
        @type: list of wx.ItemContainer objects
        """
        self.follow_choice = []
        """Keeps track of the ItemContainer objects that contain lists of verb names.
        @type: list of wx.ItemContainer objects
        """
        
        # Contextual name (StaticText)
        context_name_st = wx.StaticText(self, wx.ID_ANY, "Contextual name")
        
        # Context name (TextCtrl)
        self.context_name_tc = wx.TextCtrl(self, wx.ID_ANY)
        """The text field containing the contextual name of the verb.
        @type: wx.TextCtrl
        """
        self.context_name_tc.Bind(wx.EVT_KILL_FOCUS, self.OnContextNameFocus)
        
        # Constant name (StaticText)
        constant_name_st = wx.StaticText(self, wx.ID_ANY, "Constant name")
        
        # Constant name (Readonly TextCtrl)
        self.constant_name_tc = wx.TextCtrl(self, wx.ID_ANY)
        """The readonly text field containing the constant name of the verb.
        @type: wx.TextCtrl
        """
        self.constant_name_tc.SetEditable(False)
        
        # Context grid sizer:
        # [ Contextual Name | <TextCtrl>
        #   Constant Name   | <TextCtrl> ]
        context_grid_sizer = wx.FlexGridSizer(2, 2, model.space, model.space)
        context_grid_sizer.SetFlexibleDirection(wx.HORIZONTAL)
        context_grid_sizer.SetNonFlexibleGrowMode(wx.FLEX_GROWMODE_NONE)
        context_grid_sizer.AddGrowableCol(1)
        context_grid_sizer.AddMany([(context_name_st, 0),
                                    (self.context_name_tc, 0, wx.EXPAND),
                                    (constant_name_st, 0),
                                    (self.constant_name_tc, 0, wx.EXPAND)])
        
        # Follower RadioButton
        self.follower_radio = wx.RadioButton(self, wx.ID_ANY, "Follower", style=wx.RB_GROUP)
        """The radio button that denotes the verb as a follower.
        @type: wx.RadioButton
        """
        self.Bind(wx.EVT_RADIOBUTTON, self.OnFollowerRadio, self.follower_radio)
        
        # Supporter RadioButton
        self.supporter_radio = wx.RadioButton(self, wx.ID_ANY, "Supporter")
        """The radio button that denotes the verb as a supporter.
        @type: wx.RadioButton
        """
        self.Bind(wx.EVT_RADIOBUTTON, self.OnFollowerRadio, self.supporter_radio)
        
        # Follower sizer: <Follower radio button>
        #                 <Supporter radio button>
        follower_sizer = wx.BoxSizer(wx.VERTICAL)
        follower_sizer.AddMany([(self.follower_radio, 0, wx.ALL, model.space),
                                (self.supporter_radio, 0, wx.ALL, model.space)])
        
        # Context sizer: [<Context grid> <Follower sizer>]
        context_sizer = wx.BoxSizer(wx.HORIZONTAL)
        context_sizer.AddMany([(context_grid_sizer, 1, wx.EXPAND|wx.ALL, model.space),
                               (follower_sizer, 0, wx.ALL, model.space)])
        
        # Precondition (StaticText)
        preconds_st = wx.StaticText(self, wx.ID_ANY, "Preconditions")
        preconds_st.SetFont(model.title_font)
        
        # AddPrecond (Button)
        add_precond_btn = wx.BitmapButton(self, wx.ID_ADD, model.add_bmp)
        add_precond_btn.SetToolTip(wx.ToolTip("Add a new precondition"))
        add_precond_btn.Bind(wx.EVT_BUTTON, self.OnAddPrecond)
        
        # TrashPrecond (Button)
        trash_precond_btn = wx.BitmapButton(self, wx.ID_UNDELETE, model.trash_bmp)
        trash_precond_btn.SetToolTip(wx.ToolTip("Restore a deleted precondition"))
        trash_precond_btn.Bind(wx.EVT_BUTTON, self.OnTrashPrecond)
        
        # Preconditions title sizer [Preconditions <Add button><Trash button>]
        preconds_title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        preconds_title_sizer.AddMany([(preconds_st, 0),
                                      ((0,0), 1, wx.EXPAND),
                                      (add_precond_btn, 0),
                                      (trash_precond_btn, 0)])
        
        # Preconditions sizer[Preconditions title sizer]
        self.preconds_sizer = wx.BoxSizer(wx.VERTICAL)
        """The sizer that manages the preconditions section.  We keep track of
        this so we can add new precondition widgets to it.
        @type: wx.BoxSizer
        """
        self.preconds_sizer.Add(preconds_title_sizer, 0, wx.EXPAND|wx.ALL, model.space)
        
        # Terminal (CheckBox)
        self.terminal_chk = wx.CheckBox(self, wx.ID_ANY, "Terminal")
        """The checkbox that denotes the verb as terminal or not.
        @type: wx.CheckBox
        """
        self.terminal_chk.Bind(wx.EVT_CHECKBOX, self.OnTerminalCheck)
        
        # Followers (StaticText)
        followers_st = wx.StaticText(self, wx.ID_ANY, "Followers")
        followers_st.SetFont(model.title_font)
        
        # AddFollower (Button)
        self.add_follower_btn = wx.BitmapButton(self, wx.ID_ADD, model.add_bmp)
        """Button used to add a follower.  We keep track of this so that we can
        disable it for terminal verbs.
        @type: wx.BitmapButton
        """
        self.add_follower_btn.SetToolTip(wx.ToolTip("Add a new follower"))
        self.add_follower_btn.Bind(wx.EVT_BUTTON, self.OnAddFollower)
        
        # TrashFollower (Button)
        self.trash_follower_btn = wx.BitmapButton(self, wx.ID_UNDELETE, model.trash_bmp)
        """Button used to restore a deleted follower.  We keep track of this so
        that we can disable it for terminal verbs.
        @type: wx.BitmapButton
        """
        self.trash_follower_btn.SetToolTip(wx.ToolTip("Restore a deleted follower"))
        self.trash_follower_btn.Bind(wx.EVT_BUTTON, self.OnTrashFollower)
        
        # Followers title sizer[<Terminal checkbox> Followers <Add button><Trash button>]
        followers_title_sizer = wx.BoxSizer(wx.HORIZONTAL)
        followers_title_sizer.AddMany([(self.terminal_chk, 0, wx.RIGHT, model.space*4),
                                       (followers_st, 0),
                                       ((0,0), 1, wx.EXPAND),
                                       (self.add_follower_btn, 0),
                                       (self.trash_follower_btn, 0)])
        
        # Follower sizer[Followers title sizer]
        self.followers_sizer = wx.BoxSizer(wx.VERTICAL)
        """The sizer that manages the followers section.  We keep track of
        this so we can add new follower widgets to it.
        @type: wx.BoxSizer
        """
        self.followers_sizer.Add(followers_title_sizer, 0, wx.EXPAND|wx.ALL, model.space)
        
        # Left sizer[Context sizer, Preconditions sizer, Followers sizer]
        left_sizer = wx.BoxSizer(wx.VERTICAL)
        left_sizer.AddMany([(context_sizer, 0, wx.EXPAND),
                            (self.preconds_sizer, 0, wx.EXPAND),
                            (self.followers_sizer, 0, wx.EXPAND)])
        
        # Actual verb (StaticText)
        actual_verb_st = wx.StaticText(self, wx.ID_ANY, "Actual verb")
        
        # Actual verb (ComboBox)
        self.actual_verb_cb = wx.ComboBox(self, wx.ID_ANY, "", style=wx.CB_DROPDOWN)
        """The combo box for the actual verb.  If the C{util_verbs.nss} file has
        been loaded, those verbs are available to be selected.  In either case,
        one can type anything in the combo box.
        @type: wx.ComboBox
        """
        self.actual_verb_cb.SetItems(model.actual_verb_names)
        self.actual_verb_cb.SetValue(self.verb.actual_name)
        self.actual_verb_cb.Bind(wx.EVT_KILL_FOCUS, self.OnActualVerbFocus)
        self.Bind(wx.EVT_COMBOBOX, self.OnActualVerbSelect, self.actual_verb_cb)
        
        # Open util_verbs (Button)
        actual_verb_btn = wx.BitmapButton(self, wx.ID_OPEN, model.open_bmp)
        actual_verb_btn.SetToolTip(wx.ToolTip("Load existing verbs from the util_verbs.nss file"))
        actual_verb_btn.Bind(wx.EVT_BUTTON, self.OnLoadVerbs)
        
        # Delete verb (Button)
        del_verb_btn = wx.BitmapButton(self, wx.ID_CLOSE, model.del_verb_bmp)
        del_verb_btn.SetToolTip(wx.ToolTip("Delete this verb"))
        del_verb_btn.Bind(wx.EVT_BUTTON, self.OnDeleteVerb)
        
        # Actual verb sizer[Actual Verb <Actual Verb ComboBox> <Open Verbs Button> <Delete Verb Button>]
        actual_verb_sizer = wx.BoxSizer(wx.HORIZONTAL)
        actual_verb_sizer.AddMany([(actual_verb_st, 0, wx.ALL, model.space),
                                   (self.actual_verb_cb, 1, wx.ALL, model.space),
                                   (actual_verb_btn, 0, wx.ALL, model.space),
                                   (del_verb_btn, 0, wx.ALL, model.space)])
        
        # Set up the other sizers that we'll add to later on.
        self.description_sizer = wx.BoxSizer(wx.VERTICAL)
        """The sizer that manages the description portion of the actual verb section.
        We keep track of this because we will need to add and remove items from it
        when the actual verb changes.
        @type: wx.BoxSizer
        """
        self.vdargs_sizer = wx.BoxSizer(wx.VERTICAL)
        """The sizer that manages the VerbData arguments portion of the actual verb section.
        We keep track of this because we will need to add and remove items from it
        when the actual verb changes.
        @type: wx.BoxSizer
        """
        self.vargs_sizer = wx.BoxSizer(wx.VERTICAL)
        """The sizer that manages the verb arguments portion of the actual verb section.
        We keep track of this because we will need to add and remove items from it
        when the actual verb changes.
        @type: wx.BoxSizer
        """
        
        # Right sizer [Actual verb sizer, Description sizer, VDargs sizer, Vargs sizer]
        right_sizer = wx.BoxSizer(wx.VERTICAL)
        right_sizer.AddMany([(actual_verb_sizer, 0, wx.EXPAND),
                            (self.description_sizer, 0, wx.EXPAND),
                            (self.vdargs_sizer, 0, wx.EXPAND),
                            (self.vargs_sizer, 0, wx.EXPAND)])
        
        # Main sizer[Left sizer, Right sizer]
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.AddMany([(left_sizer, 1, wx.EXPAND|wx.ALL, model.space),
                       (right_sizer, 1, wx.EXPAND|wx.ALL, model.space)])
        
        # Load the data from our verb to put in the widgets we set up.
        self.__load()
        self.SetSizer(sizer)
        self.SetAutoLayout(True)
    
    def __load(self):
        """Load information from the model to populate our widgets."""
        
        # Context name TextCtrl
        self.context_name_tc.SetValue(self.verb.context_name)
        
        # Constant name TextCtrl
        self.constant_name_tc.SetValue(self.verb.constant_name)
        
        # Follower/Supporter RadioButtons
        if self.verb.follower == True:
            self.follower_radio.SetValue(True)
        else:
            self.supporter_radio.SetValue(True)
        
        # If our verb already has preconditions, show them.
        for precondition in self.verb.preconditions:
            self.AddPrecondToPanel(precondition)
        
        # If our verb already has followers, show them.
        for follower in self.verb.followers:
            self.AddFollowerToPanel(follower)
        
        # Terminal CheckBox
        self.terminal_chk.SetValue(self.verb.terminal)
        self.ChangeTerminal(self.verb.terminal)
        
        # If we've loaded the util_verbs.nss file already (which, if options are set,
        # will be done when the tool loads), then we can have the UI look as we want it.
        if model.actual_verb_names.count(self.verb.actual_name) > 0:
            ix = model.actual_verb_names.index(self.verb.actual_name)
            self.AddActualVerbWidgets(model.actual_verbs[ix])
        # Otherwise, we'll make sure we show everything, but it won't be very descriptive.
        else:
            # Add widgets for each vdarg
            for ix in range(len(self.verb.vdarguments)):
                self.AddVDArgWidgets(ix, "VerbData Argument %d" % (ix+1))
            # Add widgets for each varg
            for ix in range(len(self.verb.varguments)):
                #(Mandatory?, Type, Name, Description)
                varg_tuple = (False, "", "Verb Argument %d" % (ix+1), "")
                self.AddVArgWidgets(ix, varg_tuple)
    
    #{ Event handlers
    
    def OnDeleteVerb(self, event):
        """Delete the current verb, and add it to the verb trash.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        # We're deleting this page, so stop the event from propogating
        event.StopPropagation()
        
        # Add to the trash
        notebook = self.GetGrandParent()
        b_splitter = notebook.GetPage(0)
        b_splitter.top.verb_trash.append(self.verb)
        # For each other verb, remove this verb as a follower if it is
        for ix in range(notebook.GetPageCount()-1):
            v_splitter = notebook.GetPage(ix+1)
            v_splitter.top.RemoveFollowers(self.verb)
        # Remove the verb from the model
        model.behaviour.verbs.remove(self.verb)
        model.UpdateVerbNames()        
        # Remove the page from the notebook
        notebook.DeletePage(notebook.GetSelection())
    
    def OnContextNameFocus(self, event):
        """Change the context name to what's currently in the context name TextCtrl.
        @param event: Event created by EVT_KILL_FOCUS.
        @type event: wx.CommandEvent
        """
        # Change spaces to underscores.
        name = self.context_name_tc.GetValue()
        name = name.replace(' ', '_')
        
        # Change the context name in the model and update the UI
        self.ChangeContextName(name)
    
    def OnFollowerRadio(self, event):
        """Change the follower-ness of the verb.
        @param event: Event created by EVT_RADIOBUTTON.
        @type event: wx.CommandEvent
        """
        self.ChangeFollower(self.follower_radio.GetValue())
    
    def OnTerminalCheck(self, event):
        """Change the terminal-ness of the verb.
        @param event: Event created by EVT_CHECKBOX.
        @type event: wx.CommandEvent
        """
        self.ChangeTerminal(event.Checked())
        
        # Refresh the GUI
        self.Layout()
        self.Refresh()
    
    def OnAddPrecond(self, event):
        """Create a precondition then add it to the panel.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        precond = "TRUE" # Default to TRUE
        self.verb.preconditions.append(precond)
        self.AddPrecondToPanel(precond)
        
        # Refresh the GUI
        self.Layout()
        self.Refresh()
    
    def OnChangePrecond(self, event):
        """Change a precondition.
        @param event: Event created by EVT_KILL_FOCUS.
        @type event: wx.CommandEvent
        """
        precond_tc = event.GetEventObject()
        precond = precond_tc.GetValue()
        
        if precond == "":
            precond = "TRUE"
            precond_tc.SetValue(text)
        
        ix = self.verb.preconditions.index(precond_tc.last_precond)
        
        if ix >= 0:
            self.verb.preconditions[ix] = precond
            precond_tc.last_precond = precond
    
    def OnDelPrecond(self, event):
        """Remove a precondition.  Add it to the trash if it contained something.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        del_btn = event.GetEventObject()
        
        # Make sure the event doesn't propogate, as we'll be destroying the event object.
        event.StopPropagation()
        
        # Get the TextCtrl associated with the button.
        precond_tc = del_btn.tc

        # If the precondition TextCtrl had something in it, add it to the trash.
        precond = precond_tc.GetValue()
        if precond != "":
            self.precond_trash.append(precond)
        
        # Remove the precondition from the verb
        self.verb.preconditions.remove(precond)
        
        # Destroy the Button and TextCtrl
        del_btn.Destroy()
        precond_tc.Destroy()
        
        # Refresh the GUI
        self.Layout()
        self.Refresh()
    
    def OnTrashPrecond(self, event):
        """Show a popup menu with the previously deleted preconditions.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        precond_menu = wx.Menu()

        precond_menu.Append(-1, "Deleted Preconditions")
        precond_menu.AppendSeparator()
        
        for ix, precond in enumerate(self.precond_trash):
            if len(precond) > model.desc_length:
                desc = precond[:model.desc_length-3] + "..."
            else:
                desc = precond            
            precond_menu.Append(ix, desc)
            precond_menu.Bind(wx.EVT_MENU, self.OnRestorePrecond, id=ix)
        
        self.PopupMenu(precond_menu)
    
    def OnRestorePrecond(self, event):
        """Restore a previous deleted precondition.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        ix = event.GetId()
        precond = self.precond_trash.pop(ix)
        
        if precond != None:
            self.verb.preconditions.append(precond)
            self.AddPrecondToPanel(precond)
            self.Layout()
            self.Refresh()
    
    def OnAddFollower(self, event):
        """Add a new follower to the verb, then add the widgets to the panel.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        follower = model.behaviour.verbs[0] # Default to the first verb
        self.verb.followers.append(follower)
        self.AddFollowerToPanel(follower)
        
        # Refresh the GUI
        self.Layout()
        self.Refresh()
    
    def OnChangeFollower(self, event):
        """Change a follower.
        @param event: Event created by EVT_CHOICE.
        @type event: wx.CommandEvent
        """
        follower_choice = event.GetEventObject()
        select = follower_choice.GetSelection()
        follower = model.behaviour.verbs[select]
        
        ix = self.verb.followers.index(follower_choice.last_follower)
        
        if ix >= 0:
            self.verb.followers[ix] = follower
            follower_choice.last_verb = follower
    
    def OnDelFollower(self, event):
        """Remove a follower.  Add it to the trash if it contained something.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        del_btn = event.GetEventObject()
        
        # Make sure the event doesn't propogate, as we'll be destroying the event object.
        event.StopPropagation()
        
        # Get the Choice associated with the button.
        follower_choice = del_btn.choice
        
        # Delete the choice from the follower_choice list.
        self.follow_choice.remove(follower_choice)
        
        # Remove the follower from the verb object
        for ix, follower in enumerate(self.verb.followers):
            if follower == follower_choice.last_follower:
                del self.verb.followers[ix]
                break
        
        # Add the selection to the trash if something was selected.
        select = follower_choice.GetSelection()
        if select != wx.NOT_FOUND:
            self.follower_trash.append(select)
        
        # Destroy the Button and TextCtrl
        del_btn.Destroy()
        follower_choice.Destroy()
        
        # Refresh the GUI
        self.Layout()
        self.Refresh()
    
    def OnTrashFollower(self, event):
        """Show a popup menu with the previously deleted followers.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        follower_menu = wx.Menu()

        follower_menu.Append(-1, "Deleted Followers")
        follower_menu.AppendSeparator()
        
        for ix, follower in enumerate(self.follower_trash):
            follower_menu.Append(ix, model.verb_names[follower])
            follower_menu.Bind(wx.EVT_MENU, self.OnRestoreFollower, id=ix)
        
        self.PopupMenu(follower_menu)
    
    def OnRestoreFollower(self, event):
        """Restore a deleted follower.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        ix = event.GetId()
        index = self.follower_trash.pop(ix)
        follower = model.behaviour.verbs[index]
        
        if follower != None:
            self.verb.followers.append(follower)
            self.AddFollowerToPanel(follower)
            
            # Refresh the GUI
            self.Layout()
            self.Refresh()
    
    def OnLoadVerbs(self, event):
        """Open a file dialog to load the util_verbs.nss file.
        @param event: Event created by EVT_BUTTON.
        @type event: wx.CommandEvent
        """
        open_dlg = wx.FileDialog(self,
                                 message="Select the util_verbs.nss file",
                                 defaultDir=os.getcwd(), 
                                 defaultFile="util_verbs.nss",
                                 style=wx.OPEN|wx.CHANGE_DIR)
        
        if open_dlg.ShowModal() == wx.ID_OK:
            path = open_dlg.GetPath()
            
            try:
                model.LoadUtilVerbs(path)
                self.actual_verb_cb.SetItems(model.actual_verb_names)
            
            except:
                fail_dlg = wx.MessageDialog(self,
                                            "Error loading the util_verbs.nss file.",
                                            "Error",
                                            wx.OK|wx.ICON_ERROR)
                fail_dlg.ShowModal()
                fail_dlg.Destroy()
        
        open_dlg.Destroy()
    
    def OnActualVerbFocus(self, event):
        """Set the actual verb based on the entered text.  This does not change
        the actual verb section's widgets.
        @param event: Event created by EVT_KILL_FOCUS.
        @type event: wx.CommandEvent
        """
        self.ChangeActualVerb(self.actual_verb_cb.GetValue())
    
    def OnActualVerbSelect(self, event):
        """Set the actual verb based on the selection, then add the associated widgets.
        @param event: Event created by EVT_COMBOBOX.
        @type event: wx.CommandEvent
        """
        self.ChangeActualVerb(self.actual_verb_cb.GetValue())
        ix = self.actual_verb_cb.GetSelection()
        actual_verb = model.actual_verbs[ix]
        self.AddActualVerbWidgets(actual_verb)
        
        # Refresh the GUI
        self.Layout()
        self.Refresh()
    
    def OnSetVDarg(self, event):
        """Set a VerbData argument based on an entered or selected value.
        @param event: Event created by EVT_COMBOBOX or EVT_KILL_FOCUS.
        @type event: wx.CommandEvent
        """
        vdarg_cb = event.GetEventObject()
        self.verb.vdarguments[vdarg_cb.vdarg_ix] = vdarg_cb.GetValue()
    
    def OnSetVarg(self, event):
        """Set a verb argument based on an entered or selected value.
        @param event: Event created by EVT_COMBOBOX or EVT_KILL_FOCUS.
        @type event: wx.CommandEvent
        """
        varg_cb = event.GetEventObject()
        self.verb.varguments[varg_cb.varg_ix] = varg_cb.GetValue()
    
    #}
    
    def RemoveFollowers(self, verb):
        """If this verb has the passed verb as a follower, delete it and the associated widgets.
        
        This is designed to be called when a verb is deleted, to keep everything consistent.
        @param verb: The follower we want to remove.
        @type verb: L{Verb}
        """
        deleted_list = []
        for ix, follower in enumerate(self.verb.followers):
            if follower == verb:
                follower_choice = self.follow_choice[ix]
                
                # Get the Choice associated with the button.
                del_btn = follower_choice.btn
                
                # Delete the choice from the follower_choice list.
                deleted_list.append(ix)
                
                # Destroy the Button and TextCtrl
                del_btn.Destroy()
                follower_choice.Destroy()
        
        for ix in deleted_list:
            del self.follow_choice[ix]
            del self.verb.followers[ix]
    
    def ChangeContextName(self, name):
        """Change the context name of the verb and update the UI.
        @param name: The new context name.
        @type name: string
        """
        self.context_name_tc.SetValue(name)
        self.verb.context_name = name
        self.constant_name_tc.SetValue(self.verb.constant_name)
        model.UpdateVerbNames()
        
        # Change the text on the tab
        notebook = self.GetGrandParent()
        notebook.SetPageText(notebook.GetSelection(), name)
    
    def ChangeFollower(self, follower):
        """Change the follower-ness of the verb and update the UI.
        @param follower: Is this verb a follower?
        @type follower: bool
        """
        self.verb.follower = follower
        
        # Refresh the constant name
        self.constant_name_tc.SetValue(self.verb.constant_name)
    
    def ChangeTerminal(self, terminal):
        """Change the terminal-ness of the verb and update the UI.
        @param terminal: Is this verb terminal?
        @type terminal: bool
        """
        self.verb.terminal = terminal
        self.add_follower_btn.Enable(terminal == False)
        self.trash_follower_btn.Enable(terminal == False)
        
        for ix in range(len(self.followers_sizer.GetChildren())-1):
            self.followers_sizer.Show(1+ix, terminal == False)
    
    def AddPrecondToPanel(self, precond):
        """Add widgets to display the precondition on the panel.
        @param precond: The precondition being added to the panel.
        @type precond: string
        """
        
        # Precondition (TextCtrl)
        precond_tc = wx.TextCtrl(self, wx.ID_ANY, precond)
        precond_tc.Bind(wx.EVT_KILL_FOCUS, self.OnChangePrecond)
        precond_tc.last_precond = precond
        
        # DelPrecond (Button)
        del_btn = wx.BitmapButton(self, wx.ID_DELETE, model.del_bmp)
        del_btn.tc = precond_tc
        del_btn.Bind(wx.EVT_BUTTON, self.OnDelPrecond)
        
        # Precond sizer[<Precond TextCtrl><Del Button>
        precond_sizer = wx.BoxSizer(wx.HORIZONTAL)
        precond_sizer.AddMany([(precond_tc, 1, wx.EXPAND|wx.ALL, model.space),
                               (del_btn, 0, wx.ALL, model.space)])
        
        # Add it to the main preconditions sizer
        self.preconds_sizer.Add(precond_sizer, 0, wx.EXPAND)
    
    def AddFollowerToPanel(self, follower):
        """Add widgets to display the follower on the panel.
        @param follower: The verb we wish to add as a follower on the panel.
        @type follower: L{Verb}
        """
        select = model.behaviour.verbs.index(follower)
        
        if select >= 0:
            # Follower (Choice)
            follower_choice = wx.Choice(self, wx.ID_ANY)
            follower_choice.SetItems(model.verb_names)
            follower_choice.SetSelection(select)
            follower_choice.last_follower = follower
            self.Bind(wx.EVT_CHOICE, self.OnChangeFollower, follower_choice)
            
            # Add the choice to the list of choices, so we can update the
            # item container when new verbs are added.
            self.follow_choice.append(follower_choice)
            
            # DelFollower (Button)
            del_btn = wx.BitmapButton(self, wx.ID_DELETE, model.del_bmp)
            del_btn.Bind(wx.EVT_BUTTON, self.OnDelFollower)
            
            # Link them
            del_btn.choice = follower_choice
            follower_choice.btn = del_btn
            
            # Follower sizer[<Follower Choice><Del Button>]
            follower_sizer = wx.BoxSizer(wx.HORIZONTAL)
            follower_sizer.AddMany([(follower_choice, 1, wx.EXPAND|wx.ALL, model.space),
                                    (del_btn, 0, wx.ALL, model.space)])
            
            # Add it to the main preconditions sizer
            self.followers_sizer.Add(follower_sizer, 0, wx.EXPAND)
    
    def AddActualVerbWidgets(self, actual_verb):
        """Add the widgets associated with the ActualVerb.
        @param actual_verb: Defines which widgets we will add to the panel.
        @type actual_verb: L{ActualVerb}
        """
        if actual_verb == None:
            return
        
        # Clear the sizers, Combobox lists and vdarg/vargs on the verb
        self.ClearActualVerbWidgets()
        
        # Description (StaticText)
        desc_title_st = wx.StaticText(self, wx.ID_ANY, "Description")
        desc_title_st.SetFont(model.title_font)
        
        # <Description> (StaticText)
        desc_st = wx.StaticText(self, wx.ID_ANY, actual_verb.description)
        
        # Add to the existing Description sizer[Description <Description>]
        self.description_sizer.AddMany([(desc_title_st, 0, wx.ALL, model.space),
                                        (desc_st, 0, wx.ALL, model.space)])
        
        # VerbData Arguments (StaticText)
        vdarguments_st = wx.StaticText(self, wx.ID_ANY, "VerbData Arguments")
        vdarguments_st.SetFont(model.title_font)
        
        # Add to the existing VDargs sizer
        self.vdargs_sizer.Add(vdarguments_st, 0, wx.ALL, model.space)
        
        # Add widgets for each vdarg
        for ix, vdarg in enumerate(actual_verb.vdarguments):
            self.AddVDArgWidgets(ix, vdarg)

        # Verb Arguments
        if len(actual_verb.varguments) > 0:
            varguments_st = wx.StaticText(self, wx.ID_ANY, "Verb Arguments")
            varguments_st.SetFont(model.title_font)
            self.vargs_sizer.Add(varguments_st, 0, wx.ALL, model.space)
        
        # Add widgets for each varg
        for ix, varg in enumerate(actual_verb.varguments):
            self.AddVArgWidgets(ix, varg)
    
    def ClearActualVerbWidgets(self):
        """Clear the ActualVerb widgets from the previous selection."""
        self.description_sizer.Clear(True)
        self.vdargs_sizer.Clear(True)
        self.vargs_sizer.Clear(True)
        self.object_cbs = []
        self.string_cbs = []
        self.int_cbs = []
        self.float_cbs = []
    
    def AddVDArgWidgets(self, ix, vdarg):
        """Add the widgets associated with a VerbData argument.
        @param ix: The index in the verb's vdarguments list.
        @type ix: int
        @param vdarg: The VerbData argument we are adding widgets for.
        @type vdarg: string
        """
        
        # <Name of vdargument> (StaticText)
        vdarg_st = wx.StaticText(self, wx.ID_ANY, vdarg)
        
        # <VDArgument> (ComboBox)
        #vdarg_cb = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_DROPDOWN, validator=NonEmptyValidator())
        vdarg_cb = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_DROPDOWN)
        vdarg_cb.SetItems(model.object_names)
        self.Bind(wx.EVT_COMBOBOX, self.OnSetVDarg, vdarg_cb)
        vdarg_cb.Bind(wx.EVT_KILL_FOCUS, self.OnSetVDarg)
        
        # Add the vdarg to the verb
        vdarg_cb.vdarg_ix = ix
        
        # If we've already got a vdarg, we'll keep it.
        if ix < len(self.verb.vdarguments):
            vdarg_cb.SetValue(self.verb.vdarguments[ix])
        elif ix == len(self.verb.vdarguments):
            vdarg_cb.SetValue("")
            self.verb.vdarguments.append("")
        
        # Add the combobox to the list of object combo boxes.
        self.object_cbs.append(vdarg_cb)
        
        # Make a sizer to hold the elements and add it to the vdarg sizer
        vdarg_sizer = wx.BoxSizer(wx.HORIZONTAL)
        vdarg_sizer.AddMany([(vdarg_st, 0, wx.ALL, model.space),
                             (vdarg_cb, 1, wx.EXPAND|wx.ALL, model.space)])
        self.vdargs_sizer.Add(vdarg_sizer, 0, wx.EXPAND)
    
    def AddVArgWidgets(self, ix, varg):
        """Add the widgets associated with a Verb argument.
        @param ix: The index in the verb's varguments list.
        @type ix: int
        @param vdarg: The verb argument we are adding widgets for.
        @type vdarg: string
        """
        
        # Strip the info from the tuple
        v_mandatory = varg[0]
        v_type = varg[1]
        v_name = varg[2]
        v_description = varg[3]
        
        # <Description> (StaticText)
        v_desc_st = wx.StaticText(self, wx.ID_ANY, v_description)
        # <Type> (StaticText)
        v_type_st = wx.StaticText(self, wx.ID_ANY, v_type)
        # <Name> (StaticText)
        v_name_st = wx.StaticText(self, wx.ID_ANY, v_name)
        # <VArgument> (ComboBox)
        varg_cb = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_DROPDOWN)
        
        #if v_mandatory == True:
        #    varg_cb = wx.ComboBox(self, wx.ID_ANY, 
        #                          style=wx.CB_DROPDOWN,
        #                          validator=NonEmptyValidator())
        #    def_text = "Mandatory"
        #else:
        #    varg_cb = wx.ComboBox(self, wx.ID_ANY, style=wx.CB_DROPDOWN)
        #    def_text = ""
        
        if v_type == "object":
            varg_cb.SetItems(model.object_names)
            self.object_cbs.append(varg_cb)
        elif v_type == "string":
            varg_cb.SetItems(model.string_names)
            self.string_cbs.append(varg_cb)
        elif v_type == "int":
            varg_cb.SetItems(model.int_names)
            self.int_cbs.append(varg_cb)
        elif v_type == "float":
            varg_cb.SetItems(model.float_names)
            self.float_cbs.append(varg_cb)
        
        # Add the varg to the verb
        varg_cb.varg_ix = ix
        
        # If we've already got a vdarg, we'll keep it.
        if ix < len(self.verb.varguments):
            varg_cb.SetValue(self.verb.varguments[ix])
        elif ix == len(self.verb.varguments):
            varg_cb.SetValue("")
            self.verb.varguments.append("")
        
        self.Bind(wx.EVT_COMBOBOX, self.OnSetVarg, varg_cb)
        varg_cb.Bind(wx.EVT_KILL_FOCUS, self.OnSetVarg)
        
        # Make a sizer to hold the elements and add it to the varg sizer
        varg_sizer = wx.BoxSizer(wx.HORIZONTAL)
        varg_sizer.AddMany([(v_type_st, 0, wx.ALL, model.space),
                            (v_name_st, 0, wx.ALL, model.space),
                            (varg_cb, 1, wx.EXPAND|wx.ALL, model.space)])
        self.vargs_sizer.AddMany([(v_desc_st, 0, wx.EXPAND|wx.ALL, model.space),
                                  (varg_sizer, 0, wx.EXPAND)])
    
    def ChangeActualVerb(self, actual_name):
        """Set the actual verb based on the passed text.  This does not change
        the actual verb section's widgets.
        @param actual_name: The name of the actual verb associated with this verb.
        @type actual_name: string
        """
        self.verb.actual_name = actual_name
    
    def UpdateState(self):
        """The UpdateState for the VerbPanel updates the Choices and Comboboxes with
        the current lists in the model."""
        for choice in self.follow_choice:
            select = choice.GetSelection()
            choice.SetItems(model.verb_names)
            choice.SetSelection(select)
        
        for object_cb in self.object_cbs:
            name = object_cb.GetValue()
            object_cb.SetItems(model.object_names)
            object_cb.SetValue(name)
        
        for string_cb in self.string_cbs:
            name = string_cb.GetValue()
            string_cb.SetItems(model.string_names)
            string_cb.SetValue(name)
            
        for int_cb in self.int_cbs:
            name = int_cb.GetValue()
            int_cb.SetItems(model.int_names)
            int_cb.SetValue(name)
            
        for float_cb in self.float_cbs:
            name = float_cb.GetValue()
            float_cb.SetItems(model.float_names)
            float_cb.SetValue(name)
        
        name = self.actual_verb_cb.GetValue()
        self.actual_verb_cb.SetItems(model.actual_verb_names)
        self.actual_verb_cb.SetValue(name)
    
class BehaviourSplitter(wx.SplitterWindow):
    """Allows the user to vary how much they see of the two sections of a behaviour tab.
    
    Behaviour tabs are divided into two portions: one for editing behaviour-wide
    objects, and one for previewing the code that the behaviour will generate.
    The splitter allows the user to see more or less of one of the two portions,
    without having to resize the whole frame."""
    def __init__(self, parent, id=wx.ID_ANY):
        """Set up the two halves of the splitter.
        @param parent: The object creating this splitter.
        @type parent: wx.Window
        @param id: An optional ID that can be passed to this splitter.
            There is no particular need to pass an id at this time.
        @type id: int
        """
        wx.SplitterWindow.__init__(self, parent, id, style=0)
        
        win_style = wx.BORDER_SIMPLE|wx.FULL_REPAINT_ON_RESIZE
        self.top = BehaviourPanel(self, style=win_style|wx.TAB_TRAVERSAL)
        """The top half of the splitter.
        @type: L{BehaviourPanel}
        """
        self.bottom = BehaviourCodePreviewPanel(self, style=win_style)
        """The bottom half of the splitter.
        @type: L{BehaviourCodePreviewPanel}
        """
        
        # Best if we ensure the user doesn't hide the panes irreversibly
        self.SetMinimumPaneSize(5)
        # We'll have the top panel grow on resizes
        self.SetSashGravity(1.0)
        
        self.SplitHorizontally(self.top, self.bottom, 320)
    
    def UpdateState(self):
        """Update each half."""
        self.top.UpdateState()
        self.bottom.UpdateState()
    
class VerbSplitter(wx.SplitterWindow):
    """Allows the user to vary how much they see of the two sections of a verb tab.
    
    Verb tabs are divided into two portions: one for editing verb options, and 
    one for previewing the code that the verb will generate.
    The splitter allows the user to see more or less of one of the two portions,
    without having to resize the whole frame."""
    def __init__(self, parent, verb, id=wx.ID_ANY):
        """Set up the two halves of the splitter.
        @param parent: The object creating this splitter.
        @type parent: wx.Window
        @param id: An optional ID that can be passed to this splitter.
            There is no particular need to pass an id at this time.
        @type id: int
        """
        wx.SplitterWindow.__init__(self, parent, id, style=0)
        
        win_style = wx.BORDER_SIMPLE|wx.FULL_REPAINT_ON_RESIZE
        self.top = VerbPanel(self, verb, style=win_style|wx.TAB_TRAVERSAL)
        """The top half of the splitter.
        @type: L{VerbPanel}
        """
        self.bottom = VerbCodePreviewPanel(self, verb, style=win_style)
        """The bottom half of the splitter.
        @type: L{VerbCodePreviewPanel}
        """
        
        # Best if we ensure the user doesn't hide the panes irreversibly
        self.SetMinimumPaneSize(5)
        # We'll have the top panel grow on resizes
        self.SetSashGravity(1.0)
        
        self.SplitHorizontally(self.top, self.bottom, -160)

    def UpdateState(self):
        """Update each half."""
        self.top.UpdateState()
        self.bottom.UpdateState()
    
class MainNoteBook(wx.Notebook):
    """The notebook that encompasses the rest of the interface."""
    def __init__(self, parent, id=wx.ID_ANY):
        """Set up the notebook options, and add the behaviour tab, as this
        tab should always be present.
        @param parent: The object creating this notebook.
        @type parent: wx.Window
        @param id: An optional ID that can be passed to this notebook.
            There is no particular need to pass an id at this time.
        @type id: int
        """
        wx.Notebook.__init__(self, parent, id, 
                             style=wx.NB_TOP)
        
        b_splitter = BehaviourSplitter(self)
        self.AddPage(b_splitter, "Behaviour")
        
        self.Bind(wx.EVT_NOTEBOOK_PAGE_CHANGED, self.OnPageChanged)
    
    #{ Event handlers
    
    def OnPageChanged(self, event):
        """When we change the notebook page, we'll call an UpdateState function on the page we changed to.
        
        This will update things like combo boxes and choices with updated lists 
        from the model.  This way, each notebook page can deal only with itself 
        and the model.
        @param event: Event created by EVT_NOTEBOOK_PAGE_CHANGED.
        @type event: wx.Event
        """
        selection = event.GetSelection()
        page = self.GetPage(selection)
        page.UpdateState()
        event.Skip()
    
    #}

class MainFrame(wx.Frame):
    """The main frame for the program, containing a menu and the notebook."""
    def __init__(self, *args, **kwargs):
        """Set up the structure for the frame and add the notebook.
        @param args: Unnamed arguments, passed to the parent class's __init__ function.
        @param kwargs: Named arguments, passed to the parent class's __init__ function.
        """
        wx.Frame.__init__(self, size=(800,600), *args, **kwargs)
        
        # Set the minimum size (320x320)
        self.SetMinSize((320, 320))
        
        # Set up the Model and Config objects
        self.__load()
        
        # Main menubar
        self.__createMainMenu()
        
        # Main notebook
        self.notebook = MainNoteBook(self, wx.ID_ANY)
        """The notebook that encompasses the rest of the interface.
        @type: L{MainNoteBook}
        """
        
        # Override the close event so we can prompt to save.
        self.Bind(wx.EVT_CLOSE, self.OnExit)
        
        self.Show(True)
    
    def __load(self):
        """Set some data into the Model and Config objects."""
        self.help_path = os.getcwd() + "\\BehaviourTool.chm"
        
        model.title_font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        model.shape_font = wx.Font(8, wx.FONTFAMILY_TELETYPE, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        model.refresh_bmp = wx.Bitmap("images/refresh.png", wx.BITMAP_TYPE_PNG)
        model.trash_bmp = wx.Bitmap("images/trash.png", wx.BITMAP_TYPE_PNG)
        model.add_bmp = wx.Bitmap("images/add.png", wx.BITMAP_TYPE_PNG)
        model.del_bmp = wx.Bitmap("images/delete.png", wx.BITMAP_TYPE_PNG)
        model.del_verb_bmp = wx.Bitmap("images/delete_verb.png", wx.BITMAP_TYPE_PNG)
        model.open_bmp = wx.Bitmap("images/open.png", wx.BITMAP_TYPE_PNG)
        
        config.read("BehaviourTool.ini")
        # We're going to put everything in an "Options" section, so if we don't have one, make it.
        if config.has_section("Options") is not True:
            config.add_section("Options")
        
        # Load up certain options if we have them
        if config.has_option("Options", "util_verbs_location"):
            try:
                path = config.get("Options", "util_verbs_location")
                model.LoadUtilVerbs(path)
            except:
                config.remove_option("Options", "util_verbs_location")
    
    def __createMainMenu(self):
        """Create the main menu for the main frame and bind the events."""
        # For the main menu
        ID_OPTIONS = wx.NewId()
        ID_HELP = wx.NewId()
        
        # File menu
        file_menu = wx.Menu()
        
        file_menu.Append(wx.ID_NEW, "&New Behaviour\tCtrl+N", "Create a new behaviour.")
        self.Bind(wx.EVT_MENU, self.OnNew, id=wx.ID_NEW)
        
        file_menu.Append(wx.ID_OPEN, "&Open Behaviour...\tCtrl+O", "Open an existing behaviour.")
        self.Bind(wx.EVT_MENU, self.OnOpen, id=wx.ID_OPEN)
        
        file_menu.Append(wx.ID_SAVE, "&Save Behaviour\tCtrl+S", "Save the current behaviour.")
        self.Bind(wx.EVT_MENU, self.OnSave, id=wx.ID_SAVE)
        
        file_menu.Append(wx.ID_SAVEAS, "Save Behaviour &In...\tAlt+S", "Save the current behaviour in a different directory.")
        self.Bind(wx.EVT_MENU, self.OnSaveIn, id=wx.ID_SAVEAS)
        
        file_menu.AppendSeparator()
        
        file_menu.Append(wx.ID_EXIT, "E&xit", "Terminate the program")
        self.Bind(wx.EVT_MENU, self.OnExit, id=wx.ID_EXIT)
        # end File menu

        # Edit menu
        edit_menu = wx.Menu()
        
        edit_menu.Append(wx.ID_UNDO, "&Undo\tCtrl+Z", "Undo a previous action.")
        self.Bind(wx.EVT_MENU, self.OnUndo, id=wx.ID_UNDO)
        
        edit_menu.Append(wx.ID_REDO, "&Redo\tCtrl+Y", "Redo a previously undone action.")
        self.Bind(wx.EVT_MENU, self.OnRedo, id=wx.ID_REDO)
        
        edit_menu.AppendSeparator()
        
        edit_menu.Append(wx.ID_CUT, "Cu&t\tCtrl+X", "Cut the currently selected text.")
        self.Bind(wx.EVT_MENU, self.OnCut, id=wx.ID_CUT)
        
        edit_menu.Append(wx.ID_COPY, "&Copy\tCtrl+C", "Copy the currently selected text.")
        self.Bind(wx.EVT_MENU, self.OnCopy, id=wx.ID_COPY)
        
        edit_menu.Append(wx.ID_PASTE, "&Paste\tCtrl+V", "Paste the previously copied text.")
        self.Bind(wx.EVT_MENU, self.OnPaste, id=wx.ID_PASTE)
        # end Edit menu
        
        # Tools menu
        tools_menu = wx.Menu()
        
        #tools_menu.Append(1, "&Test Behaviour", "Test the current behaviour.")
        #self.Bind(wx.EVT_MENU, self.OnTest, id=1)
        
        tools_menu.Append(ID_OPTIONS, "&Options...", "Configure the Behaviour Tool.")
        self.Bind(wx.EVT_MENU, self.OnOptions, id=ID_OPTIONS)
        # end Tools menu
        
        # Help menu
        help_menu = wx.Menu()
        
        help_menu.Append(ID_HELP, "&Help Contents\tF1", "View the helpful documentation for the Behaviour Tool.")
        self.Bind(wx.EVT_MENU, self.OnHelp, id=ID_HELP)
        
        help_menu.AppendSeparator()
        
        help_menu.Append(wx.ID_ABOUT, "&About Behaviour Tool", "About Behaviour Tool")
        self.Bind(wx.EVT_MENU, self.OnAbout, id=wx.ID_ABOUT)        
        # end Help menu
        
        # Main menu bar
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File");
        menu_bar.Append(edit_menu, "&Edit");
        menu_bar.Append(tools_menu, "&Tools");
        menu_bar.Append(help_menu, "&Help");
        self.SetMenuBar(menu_bar)
    
    #{ Event handlers
    
    def OnNew(self, event):
        """Prompts to save, then starts a new behaviour if desired.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        if self.PromptToSave() == True:
            model.behaviour = Codegen.Behaviour()
            model.UpdateVerbNames()
            model.UpdateNWVarNames()
            self.notebook.DeleteAllPages()
            b_splitter = BehaviourSplitter(self.notebook)
            self.notebook.AddPage(b_splitter, "Behaviour")
            size = self.GetSize()
            b_splitter.SetSashPosition(size[1]*0.5)
    
    def OnOpen(self, event):
        """Prompts to save, then loads an existing behaviour.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        if self.PromptToSave() == True:
            open_dlg = wx.FileDialog(self,
                                     message="Select the b_<behaviour>.nss file",
                                     defaultDir=os.getcwd(), 
                                     style=wx.OPEN|wx.CHANGE_DIR)
            
            if open_dlg.ShowModal() == wx.ID_OK:
                path = open_dlg.GetPath()
                
                try:
                    model.behaviour = Io.LoadBehaviour(path)
                    model.UpdateVerbNames()
                    model.UpdateNWVarNames()
                    self.notebook.DeleteAllPages()
                    b_splitter = BehaviourSplitter(self.notebook)
                    self.notebook.AddPage(b_splitter, model.behaviour.name)
                    size = self.GetSize()
                    b_splitter.SetSashPosition(size[1]*0.5)
                    
                    for verb in model.behaviour.verbs:
                        v_splitter = VerbSplitter(self.notebook, verb)
                        self.notebook.AddPage(v_splitter, verb.context_name)
                except:
                    fail_dlg = wx.MessageDialog(self,
                                                "%s is not a valid behaviour script!" % os.path.basename(path),
                                                "Error",
                                                wx.OK|wx.ICON_ERROR)
                    fail_dlg.ShowModal()
                    fail_dlg.Destroy()
            
            open_dlg.Destroy()
    
    def OnSave(self, event):
        """Save the behaviour; if possible, use the current working directory.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        self.SaveBehaviour(False)
    
    def OnSaveIn(self, event):
        """Save the behaviour; always prompt the user to select a directory.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        self.SaveBehaviour(True)
    
    def OnExit(self, event):
        """Prompt to save, then destroy the window on Yes or No.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        # Save the config options
        FILE = open("BehaviourTool.ini", 'w')
        config.write(FILE)
        FILE.close()
        
        if self.PromptToSave() == True:
            self.Destroy()
        else:
            event.Veto()
    
    def OnUndo(self, event):
        """Call the Undo method of the currently focused window.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        focused = wx.Window_FindFocus()
        focused.Undo()

    def OnRedo(self, event):
        """Call the Redo method of the currently focused window.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        focused = wx.Window_FindFocus()
        focused.Redo()

    def OnCut(self, event):
        """Call the Cut method of the currently focused window.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        focused = wx.Window_FindFocus()
        focused.Cut()

    def OnCopy(self, event):
        """Call the Copy method of the currently focused window.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        focused = wx.Window_FindFocus()
        focused.Copy()

    def OnPaste(self, event):
        """Call the Paste method of the currently focused window.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        focused = wx.Window_FindFocus()
        focused.Paste()
    
    #def OnTest(self, event):
    #    pass
    
    def OnOptions(self, event):
        """Show the L{BOptionsDialog} to allow the user to edit program options.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        options_dlg = BOptionsDialog(self)
        options_dlg.CenterOnScreen()
        
        rc = options_dlg.ShowModal()
        
        if rc == wx.ID_OK:
            options_dlg.UpdateConfig()
        
        options_dlg.Destroy()
    
    def OnHelp(self, event):
        """Show the documentation.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        os.startfile(self.help_path)
    
    def OnAbout(self, event):
        """Show information about the program.
        @param event: Event created by EVT_MENU.
        @type event: wx.CommandEvent
        """
        # First we create and fill the info object
        info = wx.AboutDialogInfo()
        info.Name = "Behaviour Tool"
        info.Version = "0.0.1"
        #info.Copyright = "(C) 2007 Trevor Bekolay"
        info.Description = "The \"Behaviour Tool\" is a tool for creating behaviours for use in the PaSSAGE framework."
        info.WebSite = ("http://ircl.cs.ualberta.ca/games/passage/", "PaSSAGE home page")
        info.Developers = ["Trevor Bekolay"]
        #info.License = "???"

        # Then we call wx.AboutBox giving it that info object
        wx.AboutBox(info)
    
    #}
    
    def SaveBehaviour(self, force):
        """Save the behaviour's script files in the current directory, or a specified directory.
        
        If you don't force the user to choose a directory, the current working
        directory will be searched for appropriate script files; that is, files
        bearing the same name as those that are going to be saved.  If those
        files are found, they will be overwritten automatically with the newly
        generated files.  If they are not found, the user will be prompted to
        select a directory.
        @param force: Should we force the user to select a directory?
        @type force: bool
        @return: Did the files save sucessfully?
        @rtype: bool
        """
        if force == False:
            base_path = os.getcwd()
            b_file = base_path + "\\b_%s.nss" % model.behaviour.name.lower()
            z_b_file = base_path + "\\z_b_%s.nss" % model.behaviour.name.lower()
            if os.path.exists(b_file) and os.path.exists(z_b_file):
                try:
                    Io.SaveBFile(b_file, model.behaviour)
                    Io.SaveZBFile(z_b_file, model.behaviour)
                    return True
                except:
                    fail_dlg = wx.MessageDialog(self,
                                                "Error saving the script files.",
                                                "Error",
                                                wx.OK|wx.ICON_ERROR)
                    fail_dlg.ShowModal()
                    fail_dlg.Destroy()
        
        dlg = wx.DirDialog(self, "Choose the directory containing your module's files.",
                           defaultPath=os.getcwd(),
                           style=wx.DD_DEFAULT_STYLE|wx.DD_CHANGE_DIR)
        rc = dlg.ShowModal()
        dlg.Destroy()
        
        # If the user clicked OK, try to save the script files.
        if rc == wx.ID_OK:
            base_path = dlg.GetPath()
            b_file = base_path + "\\b_%s.nss" % model.behaviour.name.lower()
            z_b_file = base_path + "\\z_b_%s.nss" % model.behaviour.name.lower()
            
            try:
                Io.SaveBFile(b_file, model.behaviour)
                Io.SaveZBFile(z_b_file, model.behaviour)
                return True
            except:
                fail_dlg = wx.MessageDialog(self,
                                            "Error saving the script files.",
                                            "Error",
                                            wx.OK|wx.ICON_ERROR)
                fail_dlg.ShowModal()
                fail_dlg.Destroy()
                return False
        
        else:
            return False    
    
    def PromptToSave(self):
        """Prompts the user to save the current behaviour.        
        @return: Did the user make a choice? (i.e., did they B{not} press C{Cancel}?)
        @rtype: bool
        """
        to_return = True
        
        if model.behaviour.name == "":
            name = "untitled"
        else:
            name = model.behaviour.name
        
        # Prompt to save first.
        dlg = wx.MessageDialog(self, "Save changes to %s?" % name,
                               "Behaviour Tool",
                               wx.YES_NO | wx.CANCEL | wx.ICON_QUESTION)
        rc = dlg.ShowModal()
        dlg.Destroy()
        
        # Save the current behaviour
        if rc == wx.ID_YES:
            to_return = self.SaveBehaviour(False)
        
        # Return True if yes or no was pressed and the save dialog wasn't cancelled.
        to_return = to_return and (rc == wx.ID_YES or rc == wx.ID_NO)
        
        return to_return

class BehaviourApp(wx.App):
    """Our program."""
    def OnInit(self):
        """Load up our L{MainFrame}.
        @return: This function needs to return a bool to indicate success; we always return True.
        @rtype: bool
        """
        ogl.OGLInitialize()
        frame = MainFrame(None, wx.ID_ANY, "Behaviour Tool")
        return True

if __name__ == '__main__':
    app = BehaviourApp(redirect=1, filename="ErrorLog.txt")
    app.MainLoop()
    
