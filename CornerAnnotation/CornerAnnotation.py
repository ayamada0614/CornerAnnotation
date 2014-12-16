import os
import unittest
from __main__ import vtk, qt, ctk, slicer

#
# CornerAnnotation
#

class CornerAnnotation:
  def __init__(self, parent):
    parent.title = "CornerAnnotation" # TODO make this more human readable by adding spaces
    parent.categories = ["IGT"]
    parent.dependencies = []
    parent.contributors = ["Atsushi Yamada (Shiga University of Medical Science in Japan), Junichi Tokuda (Brigham and Women's Hospital), Koichiro Murakami (SUMS), Soichiro Tani (BWH, SUMS), Shigeyuki Naka (SUMS), Tohru Tani (SUMS)"] # replace with "Firstname Lastname (Org)"
    parent.helpText = """
    This module allows user to create annotations including timer count and transform node elements and display them. The details are in <a href=http://www.slicer.org/slicerWiki/index.php/Documentation/Nightly/Modules/CornerAnnotation>the online documentation</a>.
    """
    parent.acknowledgementText = """
    This work is supported by Bio-Medical Innovation Center and Department of Surgery, Shiga University of Medical Science in Japan. 
""" # replace with organization, grant and thanks.
    self.parent = parent

    # Add this test to the SelfTest module's list for discovery when the module
    # is created.  Since this module may be discovered before SelfTests itself,
    # create the list if it doesn't already exist.
    try:
      slicer.selfTests
    except AttributeError:
      slicer.selfTests = {}
    slicer.selfTests['CornerAnnotation'] = self.runTest

  def runTest(self):
    tester = CornerAnnotationTest()
    tester.runTest()

#
# qCornerAnnotationWidget
#

class CornerAnnotationWidget:
  def __init__(self, parent = None):
    if not parent:
      self.parent = slicer.qMRMLWidget()
      self.parent.setLayout(qt.QVBoxLayout())
      self.parent.setMRMLScene(slicer.mrmlScene)
    else:
      self.parent = parent
    self.layout = self.parent.layout()
    if not parent:
      self.setup()
      self.parent.show()

  def setup(self):
    # Instantiate and connect widgets ...

    #
    # Reload and Test area
    #
    reloadCollapsibleButton = ctk.ctkCollapsibleButton()
    reloadCollapsibleButton.text = "Reload && Test"
    #self.layout.addWidget(reloadCollapsibleButton)
    reloadFormLayout = qt.QFormLayout(reloadCollapsibleButton)

    # reload button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadButton = qt.QPushButton("Reload")
    self.reloadButton.toolTip = "Reload this module."
    self.reloadButton.name = "CornerAnnotation Reload"
    #reloadFormLayout.addWidget(self.reloadButton)
    self.reloadButton.connect('clicked()', self.onReload)

    # reload and test button
    # (use this during development, but remove it when delivering
    #  your module to users)
    self.reloadAndTestButton = qt.QPushButton("Reload and Test")
    self.reloadAndTestButton.toolTip = "Reload this module and then run the self tests."
    #reloadFormLayout.addWidget(self.reloadAndTestButton)
    self.reloadAndTestButton.connect('clicked()', self.onReloadAndTest)

    #
    # Module Area
    #
    annotationCollapsibleButton = ctk.ctkCollapsibleButton()
    annotationCollapsibleButton.text = "Annotations"
    annotationCollapsibleButton.collapsed = False
    self.annotationList = annotationCollapsibleButton   
    self.layout.addWidget(annotationCollapsibleButton)

    # Layout within the collapsible button
    annotationFormLayout = qt.QFormLayout(annotationCollapsibleButton)

    #
    # Transform matrix for left bottom annotation (vtkMRMLLinearTransformNode)
    #
    self.node1Selector = slicer.qMRMLNodeComboBox()
    #self.node1Selector.nodeTypes = ( ("vtkMRMLLinearTransformNode"), "" )
    self.node1Selector.nodeTypes = ['vtkMRMLLinearTransformNode', 'vtkMRMLAnnotationTextNode']
    self.node1Selector.addEnabled = False
    self.node1Selector.removeEnabled = False
    self.node1Selector.noneEnabled =  True
    self.node1Selector.showHidden = False
    self.node1Selector.showChildNodeTypes = False
    self.node1Selector.setMRMLScene( slicer.mrmlScene )

    #
    # Transform matrix for left upper annotation (vtkMRMLLinearTransformNode)
    #
    self.node2Selector = slicer.qMRMLNodeComboBox()
    self.node2Selector.nodeTypes = ['vtkMRMLLinearTransformNode', 'vtkMRMLAnnotationTextNode']
    self.node2Selector.addEnabled = False
    self.node2Selector.removeEnabled = False
    self.node2Selector.noneEnabled =  True
    self.node2Selector.showHidden = False
    self.node2Selector.showChildNodeTypes = False
    self.node2Selector.setMRMLScene( slicer.mrmlScene )

    #
    # Transform matrix for left upper annotation (vtkMRMLLinearTransformNode)
    #
    self.node3Selector = slicer.qMRMLNodeComboBox()
    self.node3Selector.nodeTypes = ['vtkMRMLLinearTransformNode', 'vtkMRMLAnnotationTextNode']
    self.node3Selector.addEnabled = False
    self.node3Selector.removeEnabled = False
    self.node3Selector.noneEnabled =  True
    self.node3Selector.showHidden = False
    self.node3Selector.showChildNodeTypes = False
    self.node3Selector.setMRMLScene( slicer.mrmlScene )

    #
    # Transform matrix for right upper annotation (vtkMRMLLinearTransformNode)
    #
    self.node4Selector = slicer.qMRMLNodeComboBox()
    self.node4Selector.nodeTypes = ['vtkMRMLLinearTransformNode', 'vtkMRMLAnnotationTextNode']
    self.node4Selector.addEnabled = False
    self.node4Selector.removeEnabled = False
    self.node4Selector.noneEnabled =  True
    self.node4Selector.showHidden = False
    self.node4Selector.showChildNodeTypes = False
    self.node4Selector.setMRMLScene( slicer.mrmlScene )

    #
    # Check box for left bottom annotation
    #
    self.leftBottomCheckBox = ctk.ctkCheckBox()
    self.leftBottomCheckBox.text = "Enable"
    self.leftBottomCheckBox.enabled = True
    self.leftBottomCheckBox.checked = False

    #
    # Check box for displaying right upper annotation
    #
    self.leftBottomTextBox = qt.QLineEdit()
    self.leftBottomTextBox.enabled = True

    #
    # Check box for displaying left upper annotation
    #
    self.leftUpperCheckBox = ctk.ctkCheckBox()
    self.leftUpperCheckBox.text = "Enable"
    self.leftUpperCheckBox.enabled = True
    self.leftUpperCheckBox.checked = False

    #
    # Check box for displaying right upper annotation
    #
    self.leftUpperTextBox = qt.QLineEdit()
    self.leftUpperTextBox.enabled = True

    #
    # Check box for displaying right bottom annotation
    #
    self.rightBottomCheckBox = ctk.ctkCheckBox()
    self.rightBottomCheckBox.text = "Enable"
    self.rightBottomCheckBox.enabled = True
    self.rightBottomCheckBox.checked = False

    #
    # Check box for displaying right upper annotation
    #
    self.rightBottomTextBox = qt.QLineEdit()
    self.rightBottomTextBox.enabled = True

    #
    # Check box for displaying right upper annotation
    #
    self.rightUpperCheckBox = ctk.ctkCheckBox()
    self.rightUpperCheckBox.text = "Enable"
    self.rightUpperCheckBox.enabled = True
    self.rightUpperCheckBox.checked = False

    #
    # Check box for displaying right upper annotation
    #
    self.rightUpperTextBox = qt.QLineEdit()
    self.rightUpperTextBox.enabled = True


    self.textLable1 = qt.QLabel()
    self.textLable1.setText("Text:")

    self.textLable2 = qt.QLabel()
    self.textLable2.setText("Text:")

    self.textLable3 = qt.QLabel()
    self.textLable3.setText("Text:")

    self.textLable4 = qt.QLabel()
    self.textLable4.setText("Text:")

    self.leftUpperFrame = qt.QFrame()
    self.leftUpperLayout = qt.QHBoxLayout()
    self.leftUpperFrame.setLayout(self.leftUpperLayout)
    annotationFormLayout.addRow("Left Upper:", self.leftUpperFrame)

    self.leftBottomFrame = qt.QFrame()
    self.leftBottomLayout = qt.QHBoxLayout()
    self.leftBottomFrame.setLayout(self.leftBottomLayout)
    annotationFormLayout.addRow("Left Bottom:", self.leftBottomFrame)

    self.rightUpperFrame = qt.QFrame()
    self.rightUpperLayout = qt.QHBoxLayout()
    self.rightUpperFrame.setLayout(self.rightUpperLayout)
    annotationFormLayout.addRow("Right Upper:", self.rightUpperFrame)

    self.rightBottomFrame = qt.QFrame()
    self.rightBottomLayout = qt.QHBoxLayout()
    self.rightBottomFrame.setLayout(self.rightBottomLayout)
    annotationFormLayout.addRow("Right Bottom:", self.rightBottomFrame)

    self.leftUpperFrame.layout().addWidget(self.leftUpperCheckBox)
    self.leftUpperFrame.layout().addWidget(self.textLable2)
    self.leftUpperFrame.layout().addWidget(self.leftUpperTextBox)

    self.leftBottomFrame.layout().addWidget(self.leftBottomCheckBox)
    self.leftBottomFrame.layout().addWidget(self.textLable1)
    self.leftBottomFrame.layout().addWidget(self.leftBottomTextBox)

    self.rightUpperFrame.layout().addWidget(self.rightUpperCheckBox)
    self.rightUpperFrame.layout().addWidget(self.textLable4)
    self.rightUpperFrame.layout().addWidget(self.rightUpperTextBox)

    self.rightBottomFrame.layout().addWidget(self.rightBottomCheckBox)
    self.rightBottomFrame.layout().addWidget(self.textLable3)
    self.rightBottomFrame.layout().addWidget(self.rightBottomTextBox)

    #
    # Configuration Area
    #
    configurationCollapsibleButton = ctk.ctkCollapsibleButton()
    configurationCollapsibleButton.text = "Configurations"
    configurationCollapsibleButton.collapsed = False
    self.annotationList = configurationCollapsibleButton   
    self.layout.addWidget(configurationCollapsibleButton)

    # Layout within the collapsible button
    configurationFormLayout = qt.QFormLayout(configurationCollapsibleButton)

    self.threeDViewCheckBox = ctk.ctkCheckBox()
    self.threeDViewCheckBox.text = "3D"
    self.threeDViewCheckBox.enabled = True
    self.threeDViewCheckBox.checked = True

    self.redViewCheckBox = ctk.ctkCheckBox()
    self.redViewCheckBox.text = "Red"
    self.redViewCheckBox.enabled = True
    self.redViewCheckBox.checked = False

    self.yellowViewCheckBox = ctk.ctkCheckBox()
    self.yellowViewCheckBox.text = "Yellow"
    self.yellowViewCheckBox.enabled = True
    self.yellowViewCheckBox.checked = False

    self.greenViewCheckBox = ctk.ctkCheckBox()
    self.greenViewCheckBox.text = "Green"
    self.greenViewCheckBox.enabled = True
    self.greenViewCheckBox.checked = False

    # view frame
    self.viewFrame = qt.QFrame(configurationCollapsibleButton)
    self.viewLayout = qt.QHBoxLayout()
    self.viewFrame.setLayout(self.viewLayout)
    configurationFormLayout.addRow("Display Panels:", self.viewFrame)

    self.viewFrame.layout().addWidget(self.threeDViewCheckBox)
    self.viewFrame.layout().addWidget(self.redViewCheckBox)
    self.viewFrame.layout().addWidget(self.yellowViewCheckBox)
    self.viewFrame.layout().addWidget(self.greenViewCheckBox)

    self.fontSizeLable = qt.QLabel()
    self.fontSizeLable.setText("Size:")

    #
    # Bold font check box for displaying right upper annotation
    #
    self.rightUpperBoldCheckBox = ctk.ctkCheckBox()
    self.rightUpperBoldCheckBox.text = "Bold"
    self.rightUpperBoldCheckBox.enabled = True
    self.rightUpperBoldCheckBox.checked = False

    #
    # Italic fong check box for displaying right upper annotation
    #
    self.rightUpperItalicCheckBox = ctk.ctkCheckBox()
    self.rightUpperItalicCheckBox.text = "Italic"
    self.rightUpperItalicCheckBox.enabled = True
    self.rightUpperItalicCheckBox.checked = False

    #
    # Shadow font check box for displaying right upper annotation
    #
    self.rightUpperShadowCheckBox = ctk.ctkCheckBox()
    self.rightUpperShadowCheckBox.text = "Shadow"
    self.rightUpperShadowCheckBox.enabled = True
    self.rightUpperShadowCheckBox.checked = False

    #
    # Font size slider
    #
    self.fontSizeSlider = ctk.ctkSliderWidget()
    self.fontSizeSlider.decimals = 0
    self.fontSizeSlider.maximum = 200
    self.fontSizeSlider.minimum = 0
    self.fontSizeSlider.value = 20
    self.fontSizeSlider.enabled = True

    self.fontBox = qt.QComboBox()
    self.fontBox.insertItem(0,"Arial", "Arial")
    self.fontBox.insertItem(1,"Courier", "Courier")
    self.fontBox.insertItem(2,"Times", "Times")
    self.fontBox.enabled = True
    configurationFormLayout.addRow("Font Family:", self.fontBox)

    self.rightUpperColorBox = ctk.ctkColorPickerButton()
    self.rightUpperColorBox.enabled = True
    self.rightUpperColorBox.setColor(qt.QColor(255,0,0))    
    configurationFormLayout.addRow("Font Color:", self.rightUpperColorBox)

    self.fontOpacitySlider = ctk.ctkSliderWidget()
    self.fontOpacitySlider.decimals = 0
    self.fontOpacitySlider.maximum = 100
    self.fontOpacitySlider.minimum = 0
    self.fontOpacitySlider.value = 100
    self.fontOpacitySlider.enabled = True
    configurationFormLayout.addRow("Font Opacity:", self.fontOpacitySlider)

    self.fontStyleFrame = qt.QFrame()
    self.fonstStyleLayout = qt.QHBoxLayout()
    self.fontStyleFrame.setLayout(self.fonstStyleLayout)
    configurationFormLayout.addRow("Font Style:", self.fontStyleFrame)

    self.fontStyleFrame.layout().addWidget(self.rightUpperBoldCheckBox)
    self.fontStyleFrame.layout().addWidget(self.rightUpperItalicCheckBox)
    self.fontStyleFrame.layout().addWidget(self.rightUpperShadowCheckBox)
    self.fontStyleFrame.layout().addWidget(self.fontSizeLable)
    self.fontStyleFrame.layout().addWidget(self.fontSizeSlider)

    # Timer start button
    self.timerStartButton = qt.QPushButton("Start")
    self.timerStartButton.toolTip = "Start timer"
    self.timerStartButton.name = "Start timer"

    # Timer stop button
    self.timerStopButton = qt.QPushButton("Stop")
    self.timerStopButton.toolTip = "Stop timer"
    self.timerStopButton.name = "Stop timer"

    # Timer reset button
    self.timerResetButton = qt.QPushButton("Reset")
    self.timerResetButton.toolTip = "Reset timer"
    self.timerResetButton.name = "Reset timer"

    self.timerFrame = qt.QFrame(configurationCollapsibleButton)
    self.timerLayout = qt.QHBoxLayout()
    self.timerFrame.setLayout(self.timerLayout)
    configurationFormLayout.addRow("Timer:", self.timerFrame)

    self.timerFrame.layout().addWidget(self.timerStartButton)
    self.timerFrame.layout().addWidget(self.timerStopButton)
    self.timerFrame.layout().addWidget(self.timerResetButton)

    configurationFormLayout.addRow("Node1: ", self.node1Selector)
    configurationFormLayout.addRow("Node2: ", self.node2Selector)
    configurationFormLayout.addRow("Node3: ", self.node3Selector)
    configurationFormLayout.addRow("Node4: ", self.node4Selector)

    self.timerStartButton.connect('clicked(bool)', self.onStartButton)
    self.timerStopButton.connect('clicked(bool)', self.onStopButton)
    self.timerResetButton.connect('clicked(bool)', self.onResetButton)

    self.fontOpacitySlider.connect('valueChanged(double)', self.fontOpacitySliderValueChanged)
    self.fontSizeSlider.connect('valueChanged(double)', self.fontSizeSliderValueChanged)
    self.rightUpperBoldCheckBox.connect('clicked(bool)', self.boldChanged)    
    self.rightUpperItalicCheckBox.connect('clicked(bool)', self.italicChanged)
    self.rightUpperShadowCheckBox.connect('clicked(bool)', self.shadowChanged)
    self.rightUpperColorBox.connect('colorChanged(QColor)', self.fontColorChanged)

    self.rightUpperCheckBox.connect('clicked(bool)', self.onRightUpperCheckBox)
    self.rightBottomCheckBox.connect('clicked(bool)', self.onRightBottomCheckBox)
    self.leftUpperCheckBox.connect('clicked(bool)', self.onLeftUpperCheckBox)
    self.leftBottomCheckBox.connect('clicked(bool)', self.onLeftBottomCheckBox)

    self.rightUpperTextBox.connect('textEdited(QString)', self.editedRightUpperTextBox)
    self.rightBottomTextBox.connect('textEdited(QString)', self.editedRightBottomTextBox)
    self.leftUpperTextBox.connect('textEdited(QString)', self.editedLeftUpperTextBox)
    self.leftBottomTextBox.connect('textEdited(QString)', self.editedLeftBottomTextBox)

    self.threeDViewCheckBox.connect('clicked(bool)', self.onThreeDViewCheckBox)
    self.redViewCheckBox.connect('clicked(bool)', self.onRedViewCheckBox)
    self.yellowViewCheckBox.connect('clicked(bool)', self.onYellowViewCheckBox)
    self.greenViewCheckBox.connect('clicked(bool)', self.onGreenViewCheckBox)

    self.fontBox.connect('currentIndexChanged(int)',self.fontChanged)

    # Text property for corner annotation
    self.textProperty = vtk.vtkTextProperty()

    # Corner annotation function
    self.cornerAnnotationDisplay = vtk.vtkCornerAnnotation()
    self.cornerAnnotationDisplay.SetLinearFontScaleFactor(2)
    self.cornerAnnotationDisplay.SetNonlinearFontScaleFactor(1)
    self.cornerAnnotationDisplay.SetMaximumFontSize(20)
    self.cornerAnnotationDisplay.GetTextProperty().SetColor(1,0,0)

   # Addition of corner annotation function to three D render window 
    layout = slicer.app.layoutManager()
    if layout != None:
        self.threeDRenderer = layout.activeThreeDRenderer()
        self.threeDRenderer.AddViewProp(self.cornerAnnotationDisplay)
        self.threeDRenderWindow = self.threeDRenderer.GetRenderWindow()
        self.threeDRenderWindow.Render()

        self.redRenderer = layout.sliceWidget('Red').sliceView().renderWindow().GetRenderers().GetFirstRenderer()
        self.redRenderWindow = self.redRenderer.GetRenderWindow()
        self.redRenderWindow.Render()

        self.yellowRenderer = layout.sliceWidget('Yellow').sliceView().renderWindow().GetRenderers().GetFirstRenderer()
        self.yellowRenderWindow = self.yellowRenderer.GetRenderWindow()
        self.yellowRenderWindow.Render()

        self.greenRenderer = layout.sliceWidget('Green').sliceView().renderWindow().GetRenderers().GetFirstRenderer()
        self.greenRenderWindow = self.greenRenderer.GetRenderWindow()
        self.greenRenderWindow.Render()

    # QTimer
    self.t = qt.QTimer();
    self.t.connect('timeout()',self.tCount)    
    self.freq = 50

    self.stopWatchTimer = qt.QTimer();
    self.stopWatchTimer.connect('timeout()',self.stopWatchTimerCount)
    self.timerCount = 0
    self.timerFreq = 100

    # Flags for displaying annotations
    self.rightUpperFlag = 0
    self.rightBottomFlag = 0
    self.leftUpperFlag = 0
    self.leftBottomFlag = 0
    self.timerStopFlag = 0

    self.colorR = 0
    self.colorG = 0
    self.colorB = 0

    self.rightUpperMessage = ""
    self.rightBottomMessage = ""
    self.leftUpperMessage = ""
    self.leftBottomMessage = ""

    self.rightUpperSource = ""
    self.rightBottomSource = ""
    self.leftUpperSource = ""
    self.leftBottomSource = ""

    import numpy 
    self.row2 = numpy.zeros([10])
    self.column2 = numpy.zeros([10])

    self.stopWatchTimerStartFlag = 0

    # Add vertical spacer
    self.layout.addStretch(1)

  def onStartButton(self):
    if(self.stopWatchTimerStartFlag == 0):
        self.stopWatchTimerStartFlag = 1
        self.stopWatchTimer.start(self.timerFreq)

  def onStopButton(self):
    if(self.stopWatchTimerStartFlag == 1):
        self.stopWatchTimer.stop()
    self.stopWatchTimerStartFlag = 0

  def onResetButton(self):
    if(self.stopWatchTimerStartFlag == 0):
        self.timerCount = 0

  def fontChanged(self, selectedFont):
    if(selectedFont == 0):
        font = "Arial"
    elif(selectedFont == 1):
        font = "Courier"
    elif(selectedFont == 2):
        font = "Times"

    self.cornerAnnotationDisplay.GetTextProperty().SetFontFamilyAsString(font)

  def onThreeDViewCheckBox(self):
    if self.threeDViewCheckBox.checked == True:
      self.threeDRenderer.AddViewProp(self.cornerAnnotationDisplay)
    else:
      self.threeDRenderer.RemoveViewProp(self.cornerAnnotationDisplay)

  def onRedViewCheckBox(self):
    if self.redViewCheckBox.checked == True:
      self.redRenderer.AddViewProp(self.cornerAnnotationDisplay)
    else:
      self.redRenderer.RemoveViewProp(self.cornerAnnotationDisplay)

  def onYellowViewCheckBox(self):
    if self.yellowViewCheckBox.checked == True:
      self.yellowRenderer.AddViewProp(self.cornerAnnotationDisplay)
    else:
      self.yellowRenderer.RemoveViewProp(self.cornerAnnotationDisplay)

  def onGreenViewCheckBox(self):
    if self.greenViewCheckBox.checked == True:
      self.greenRenderer.AddViewProp(self.cornerAnnotationDisplay)
    else:
      self.greenRenderer.RemoveViewProp(self.cornerAnnotationDisplay)

  def editedRightUpperTextBox(self, inputText):
    self.rightUpperSource = inputText

  def editedRightBottomTextBox(self, inputText):
    self.rightBottomSource = inputText

  def editedLeftUpperTextBox(self, inputText):
    self.leftUpperSource = inputText

  def editedLeftBottomTextBox(self, inputText):
    self.leftBottomSource = inputText

  def onRightUpperCheckBox(self):
    if self.rightUpperCheckBox.checked == True:
      self.rightUpperFlag = 1
      if self.t.isActive() == 0:
        self.t.start(self.freq)
    else:
      self.rightUpperFlag = 0
      if self.rightBottomCheckBox.checked == False and self.leftUpperCheckBox.checked == False and self.leftBottomCheckBox.checked == False and self.t.isActive() == 1:
        self.timerStopFlag = 1

  def onRightBottomCheckBox(self):
    if self.rightBottomCheckBox.checked == True:
      self.rightBottomFlag = 1
      if self.t.isActive() == 0:
        self.t.start(self.freq)
    else:
      self.rightBottomFlag = 0
      if self.rightUpperCheckBox.checked == False and self.leftUpperCheckBox.checked == False and self.leftBottomCheckBox.checked == False and self.t.isActive() == 1:
        self.timerStopFlag = 1

  def onLeftUpperCheckBox(self):
    if self.leftUpperCheckBox.checked == True:
      self.leftUpperFlag = 1
      if self.t.isActive() == 0:
        self.t.start(self.freq)
    else:
      self.leftUpperFlag = 0
      if self.rightBottomCheckBox.checked == False and self.rightUpperCheckBox.checked == False and self.leftBottomCheckBox.checked == False and self.t.isActive() == 1:
        self.timerStopFlag = 1

  def onLeftBottomCheckBox(self):
    if self.leftBottomCheckBox.checked == True:
      self.leftBottomFlag = 1
      if self.t.isActive() == 0:
        self.t.start(self.freq)
    else:
      self.leftBottomFlag = 0
      if self.rightUpperCheckBox.checked == False and self.leftUpperCheckBox.checked == False and self.rightBottomCheckBox.checked == False and self.t.isActive() == 1:
        self.timerStopFlag = 1

  def fontColorChanged(self,color):
    print(color)
    red, green, blue = color.red(), color.green(), color.blue()
    
    self.colorR = round(red/255.0, 1)
    self.colorG = round(green/255.0, 1)
    self.colorB = round(blue/255.0, 1)

    self.cornerAnnotationDisplay.GetTextProperty().SetColor(self.colorR,self.colorG,self.colorB)

    print(self.colorR)
    print(self.colorG)
    print(self.colorB)

  def boldChanged(self):
    if self.rightUpperBoldCheckBox.checked == True:
      self.cornerAnnotationDisplay.GetTextProperty().BoldOn()
    else:
      self.cornerAnnotationDisplay.GetTextProperty().BoldOff()

  def italicChanged(self):
    if self.rightUpperItalicCheckBox.checked == True:
      self.cornerAnnotationDisplay.GetTextProperty().ItalicOn()
    else:
      self.cornerAnnotationDisplay.GetTextProperty().ItalicOff()

  def shadowChanged(self):
    if self.rightUpperShadowCheckBox.checked == True:
      self.cornerAnnotationDisplay.GetTextProperty().ShadowOn()
    else:
      self.cornerAnnotationDisplay.GetTextProperty().ShadowOff()

  def fontSizeSliderValueChanged(self, fontSizeValue):
    self.cornerAnnotationDisplay.SetMaximumFontSize(int(fontSizeValue))

  def fontOpacitySliderValueChanged(self, fontOpacityValue):
    self.cornerAnnotationDisplay.GetTextProperty().SetOpacity(fontOpacityValue/100)

  def makeStrings(self, gotText):

    timerCheck = gotText.find("@t")
    if timerCheck != -1:
        timerString = str(float(self.timerCount/10.0)) + "(s)"
        gotText = gotText.replace("@t", timerString)    

    splitText = gotText.split('@n')
    number = len(splitText)

    Message = ""
    for i in range(number):
      if i == number -1:
        Message += splitText[i]
      else:
        Message += splitText[i] + '\n' 

    nodeSelect1 = 0
    nodeSelect2 = 0
    nodeSelect3 = 0
    nodeSelect4 = 0

    if(self.node1Selector.currentNode() != None):
        nodeSelect1 = 1
    else:
        nodeSelect1 = 0
    if(self.node2Selector.currentNode() != None):
        nodeSelect2 = 1
    else:
        nodeSelect2 = 0
    if(self.node3Selector.currentNode() != None):
        nodeSelect3 = 1        
    else:
        nodeSelect3 = 0
    if(self.node4Selector.currentNode() != None):
        nodeSelect4 = 1        
    else:
        nodeSelect4 = 0

    if(nodeSelect1 + nodeSelect2 + nodeSelect3 + nodeSelect4 > 0):
      getElement = Message.split('[')
      numberOfElement = len(getElement)

      Message = ""
      
      for i in range(numberOfElement):
        check = getElement[i].find("]")
        if check != -1:
          nodeNumber = int(getElement[i][0])
          row = int(getElement[i][2])
          column = int(getElement[i][3])
          element = 0

          if(nodeNumber == 1 and nodeSelect1 == 1):
            element = self.node1Selector.currentNode().GetMatrixTransformToParent().GetElement(row ,column)
          
          if(nodeNumber == 2  and nodeSelect2 == 1):
            element = self.node2Selector.currentNode().GetMatrixTransformToParent().GetElement(row ,column)
          
          if(nodeNumber == 3  and nodeSelect3 == 1):
            element = self.node3Selector.currentNode().GetMatrixTransformToParent().GetElement(row ,column)
          
          if(nodeNumber == 4  and nodeSelect4 == 1):
            element = self.node4Selector.currentNode().GetMatrixTransformToParent().GetElement(row ,column)
          
          getElement[i] = getElement[i].replace("[", "")
          getElement[i] = getElement[i].replace(getElement[i][0:5], str(round(element,1)))
        Message += getElement[i]

    return (Message) 

  def tCount(self):

    # If "Slice View Annotations" is checked, the corner annoatations except the 3D view will be disabled.   
    if slicer.modules.DataProbeInstance.infoWidget.sliceAnnotations.sliceViewAnnotationsCheckBox.checked == True:

      if self.redViewCheckBox.enabled == True:
        self.redViewCheckBox.enabled = False
        self.yellowViewCheckBox.enabled = False
        self.greenViewCheckBox.enabled = False

        if self.redViewCheckBox.checked == True:
            self.redRenderer.RemoveViewProp(self.cornerAnnotationDisplay)
        if self.yellowViewCheckBox.checked == True:
            self.yellowRenderer.RemoveViewProp(self.cornerAnnotationDisplay)
        if self.greenViewCheckBox.checked == True:
            self.greenRenderer.RemoveViewProp(self.cornerAnnotationDisplay)
    else:
      if self.redViewCheckBox.enabled == False:
        self.redViewCheckBox.enabled = True
        self.yellowViewCheckBox.enabled = True
        self.greenViewCheckBox.enabled = True

        if self.redViewCheckBox.checked == True:
            self.redRenderer.AddViewProp(self.cornerAnnotationDisplay)
        if self.yellowViewCheckBox.checked == True:
            self.yellowRenderer.AddViewProp(self.cornerAnnotationDisplay)
        if self.greenViewCheckBox.checked == True:
            self.greenRenderer.AddViewProp(self.cornerAnnotationDisplay)

    if self.rightUpperFlag + self.rightBottomFlag + self.leftUpperFlag + self.leftBottomFlag < 4:
      self.cornerAnnotationDisplay.ClearAllTexts()

    if self.leftBottomFlag == 1:
      self.leftBottomMessage = self.makeStrings(self.leftBottomSource)
      self.cornerAnnotationDisplay.SetText(0, self.leftBottomMessage)

    if self.rightBottomFlag == 1:
      self.rightBottomMessage = self.makeStrings(self.rightBottomSource)
      self.cornerAnnotationDisplay.SetText(1, self.rightBottomMessage)

    if self.leftUpperFlag == 1:
      self.leftUpperMessage = self.makeStrings(self.leftUpperSource)
      self.cornerAnnotationDisplay.SetText(2, self.leftUpperMessage)

    if self.rightUpperFlag == 1:
      self.rightUpperMessage = self.makeStrings(self.rightUpperSource)
      self.cornerAnnotationDisplay.SetText(3, self.rightUpperMessage)

    self.threeDRenderWindow.Render()
    self.redRenderWindow.Render()
    self.yellowRenderWindow.Render()
    self.greenRenderWindow.Render()

    if self.timerStopFlag == 1:
      self.timerStopFlag = 0
      self.t.stop()

  def stopWatchTimerCount(self):
    self.timerCount = self.timerCount + 1

  def cleanup(self):
    pass

  def onSelect(self):
    self.applyButton.enabled = self.inputSelector.currentNode() and self.outputSelector.currentNode()

  def onApplyButton(self):
    logic = CornerAnnotationLogic()
    enableScreenshotsFlag = self.enableScreenshotsFlagCheckBox.checked
    screenshotScaleFactor = int(self.screenshotScaleFactorSliderWidget.value)
    print("Run the algorithm")
    logic.run(self.inputSelector.currentNode(), self.outputSelector.currentNode(), enableScreenshotsFlag,screenshotScaleFactor)

  def onReload(self,moduleName="CornerAnnotation"):
    """Generic reload method for any scripted module.
    ModuleWizard will subsitute correct default moduleName.
    """
    import imp, sys, os, slicer

    widgetName = moduleName + "Widget"

    # reload the source code
    # - set source file path
    # - load the module to the global space
    filePath = eval('slicer.modules.%s.path' % moduleName.lower())
    p = os.path.dirname(filePath)
    if not sys.path.__contains__(p):
      sys.path.insert(0,p)
    fp = open(filePath, "r")
    globals()[moduleName] = imp.load_module(
        moduleName, fp, filePath, ('.py', 'r', imp.PY_SOURCE))
    fp.close()

    # rebuild the widget
    # - find and hide the existing widget
    # - create a new widget in the existing parent
    parent = slicer.util.findChildren(name='%s Reload' % moduleName)[0].parent().parent()
    for child in parent.children():
      try:
        child.hide()
      except AttributeError:
        pass
    # Remove spacer items
    item = parent.layout().itemAt(0)
    while item:
      parent.layout().removeItem(item)
      item = parent.layout().itemAt(0)

    # delete the old widget instance
    if hasattr(globals()['slicer'].modules, widgetName):
      getattr(globals()['slicer'].modules, widgetName).cleanup()

    # create new widget inside existing parent
    globals()[widgetName.lower()] = eval(
        'globals()["%s"].%s(parent)' % (moduleName, widgetName))
    globals()[widgetName.lower()].setup()
    setattr(globals()['slicer'].modules, widgetName, globals()[widgetName.lower()])

  def onReloadAndTest(self,moduleName="CornerAnnotation"):
    try:
      self.onReload()
      evalString = 'globals()["%s"].%sTest()' % (moduleName, moduleName)
      tester = eval(evalString)
      tester.runTest()
    except Exception, e:
      import traceback
      traceback.print_exc()
      qt.QMessageBox.warning(slicer.util.mainWindow(), 
          "Reload and Test", 'Exception!\n\n' + str(e) + "\n\nSee Python Console for Stack Trace")


#
# CornerAnnotationLogic
#

class CornerAnnotationLogic:
  """This class should implement all the actual 
  computation done by your module.  The interface 
  should be such that other python code can import
  this class and make use of the functionality without
  requiring an instance of the Widget
  """
  def __init__(self):
    pass

  def hasImageData(self,volumeNode):
    """This is a dummy logic method that 
    returns true if the passed in volume
    node has valid image data
    """
    if not volumeNode:
      print('no volume node')
      return False
    if volumeNode.GetImageData() == None:
      print('no image data')
      return False
    return True

  def delayDisplay(self,message,msec=1000):
    #
    # logic version of delay display
    #
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def takeScreenshot(self,name,description,type=-1):
    # show the message even if not taking a screen shot
    self.delayDisplay(description)

    if self.enableScreenshots == 0:
      return

    lm = slicer.app.layoutManager()
    # switch on the type to get the requested window
    widget = 0
    if type == -1:
      # full window
      widget = slicer.util.mainWindow()
    elif type == slicer.qMRMLScreenShotDialog().FullLayout:
      # full layout
      widget = lm.viewport()
    elif type == slicer.qMRMLScreenShotDialog().ThreeD:
      # just the 3D window
      widget = lm.threeDWidget(0).threeDView()
    elif type == slicer.qMRMLScreenShotDialog().Red:
      # red slice window
      widget = lm.sliceWidget("Red")
    elif type == slicer.qMRMLScreenShotDialog().Yellow:
      # yellow slice window
      widget = lm.sliceWidget("Yellow")
    elif type == slicer.qMRMLScreenShotDialog().Green:
      # green slice window
      widget = lm.sliceWidget("Green")

    # grab and convert to vtk image data
    qpixMap = qt.QPixmap().grabWidget(widget)
    qimage = qpixMap.toImage()
    imageData = vtk.vtkImageData()
    slicer.qMRMLUtils().qImageToVtkImageData(qimage,imageData)

    annotationLogic = slicer.modules.annotations.logic()
    annotationLogic.CreateSnapShot(name, description, type, self.screenshotScaleFactor, imageData)

  def run(self,inputVolume,outputVolume,enableScreenshots=0,screenshotScaleFactor=1):
    """
    Run the actual algorithm
    """

    self.delayDisplay('Running the aglorithm')

    self.enableScreenshots = enableScreenshots
    self.screenshotScaleFactor = screenshotScaleFactor

    self.takeScreenshot('CornerAnnotation-Start','Start',-1)

    return True


class CornerAnnotationTest(unittest.TestCase):
  """
  This is the test case for your scripted module.
  """

  def delayDisplay(self,message,msec=1000):
    """This utility method displays a small dialog and waits.
    This does two things: 1) it lets the event loop catch up
    to the state of the test so that rendering and widget updates
    have all taken place before the test continues and 2) it
    shows the user/developer/tester the state of the test
    so that we'll know when it breaks.
    """
    print(message)
    self.info = qt.QDialog()
    self.infoLayout = qt.QVBoxLayout()
    self.info.setLayout(self.infoLayout)
    self.label = qt.QLabel(message,self.info)
    self.infoLayout.addWidget(self.label)
    qt.QTimer.singleShot(msec, self.info.close)
    self.info.exec_()

  def setUp(self):
    """ Do whatever is needed to reset the state - typically a scene clear will be enough.
    """
    slicer.mrmlScene.Clear(0)

  def runTest(self):
    """Run as few or as many tests as needed here.
    """
    self.setUp()
    self.test_CornerAnnotation()

  def test_CornerAnnotation(self):
    """ Ideally you should have several levels of tests.  At the lowest level
    tests sould exercise the functionality of the logic with different inputs
    (both valid and invalid).  At higher levels your tests should emulate the
    way the user would interact with your code and confirm that it still works
    the way you intended.
    One of the most important features of the tests is that it should alert other
    developers when their changes will have an impact on the behavior of your
    module.  For example, if a developer removes a feature that you depend on,
    your test should break so they know that the feature is needed.
    """

    self.delayDisplay("Starting the test")
    #
    # first, get some data
    #
    import urllib
    downloads = (
        ('http://slicer.kitware.com/midas3/download?items=5767', 'FA.nrrd', slicer.util.loadVolume),
        )

    for url,name,loader in downloads:
      filePath = slicer.app.temporaryPath + '/' + name
      if not os.path.exists(filePath) or os.stat(filePath).st_size == 0:
        print('Requesting download %s from %s...\n' % (name, url))
        urllib.urlretrieve(url, filePath)
      if loader:
        print('Loading %s...\n' % (name,))
        loader(filePath)
    self.delayDisplay('Finished with download and loading\n')

    volumeNode = slicer.util.getNode(pattern="FA")
    logic = CornerAnnotationLogic()
    self.assertTrue( logic.hasImageData(volumeNode) )
    self.delayDisplay('Test passed!')
