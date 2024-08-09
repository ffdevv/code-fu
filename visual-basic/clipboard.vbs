'*********  Code Start  ************
' This code was originally written by Terry Kreft.
' It is not to be altered or distributed,
' except as part of an application.
' You are free to use it in any application,
' provided the copyright notice is left unchanged.
'
' Code Courtesy of
' Terry Kreft
'

' from http://access.mvps.org/access/api/api0049.htm

Public Const GHND = &H42
Public Const CF_TEXT = 1
Private Const CF_ANSIONLY = &H400&
Private Const CF_APPLY = &H200&
Private Const CF_BITMAP = 2
Private Const CF_DIB = 8
Private Const CF_DIF = 5
Private Const CF_DSPBITMAP = &H82
Private Const CF_DSPENHMETAFILE = &H8E
Private Const CF_DSPMETAFILEPICT = &H83
Private Const CF_DSPTEXT = &H81
Private Const CF_EFFECTS = &H100&
Private Const CF_ENABLEHOOK = &H8&
Private Const CF_ENABLETEMPLATE = &H10&
Private Const CF_ENABLETEMPLATEHANDLE = &H20&
Private Const CF_ENHMETAFILE = 14
Private Const CF_FIXEDPITCHONLY = &H4000&
Private Const CF_FORCEFONTEXIST = &H10000
Private Const CF_GDIOBJFIRST = &H300
Private Const CF_GDIOBJLAST = &H3FF
Private Const CF_HDROP = 15
Private Const CF_INITTOLOGFONTSTRUCT = &H40&
Private Const CF_LIMITSIZE = &H2000&
Private Const CF_LOCALE = 16
Private Const CF_MAX = 17
Private Const CF_METAFILEPICT = 3
Private Const CF_NOFACESEL = &H80000
Private Const CF_NOSCRIPTSEL = &H800000
Private Const CF_NOSIMULATIONS = &H1000&
Private Const CF_NOSIZESEL = &H200000
Private Const CF_NOSTYLESEL = &H100000
Private Const CF_NOVECTORFONTS = &H800&
Private Const CF_NOOEMFONTS = CF_NOVECTORFONTS
Private Const CF_NOVERTFONTS = &H1000000
Private Const CF_OEMTEXT = 7
Private Const CF_OWNERDISPLAY = &H80
Private Const CF_PALETTE = 9
Private Const CF_PENDATA = 10
Private Const CF_PRINTERFONTS = &H2
Private Const CF_PRIVATEFIRST = &H200
Private Const CF_PRIVATELAST = &H2FF
Private Const CF_RIFF = 11
Private Const CF_SCALABLEONLY = &H20000
Private Const CF_SCREENFONTS = &H1
Private Const CF_BOTH = (CF_SCREENFONTS Or CF_PRINTERFONTS)
Private Const CF_SCRIPTSONLY = CF_ANSIONLY
Private Const CF_SELECTSCRIPT = &H400000
Private Const CF_SHOWHELP = &H4&
Private Const CF_SYLK = 4
Private Const CF_TIFF = 6
Private Const CF_TTONLY = &H40000
Private Const CF_UNICODETEXT = 13
Private Const CF_USESTYLE = &H80&
Private Const CF_WAVE = 12
Private Const CF_WYSIWYG = &H8000

Private Declare Function GlobalAlloc Lib "kernel32" (ByVal wFlags&, ByVal _
  dwBytes As Long) As Long
Private Declare Function GlobalLock Lib "kernel32" (ByVal hMem As Long) _
  As Long
Private Declare Function GlobalSize Lib "kernel32" (ByVal hMem As Long) _
  As Long
Private Declare Function lstrcpy Lib "kernel32" (ByVal lpString1 As Any, _
  ByVal lpString2 As Any) As Long
Private Declare Function lstrlen Lib "kernel32" Alias "lstrlenA" _
  (ByVal lpString As String) As Long

Private Declare Function GlobalUnlock Lib "kernel32" (ByVal hMem As Long) _
  As Long

Private Declare Function OpenClipboard Lib "user32" (ByVal Hwnd As Long) _
  As Long
Private Declare Function CloseClipboard Lib "user32" () As Long
Private Declare Function GetClipboardData Lib "user32" (ByVal wFormat As _
  Long) As Long
Private Declare Function EmptyClipboard Lib "user32" () As Long
Private Declare Function SetClipboardData Lib "user32" (ByVal wFormat _
  As Long, ByVal hMem As Long) As Long

Function ClipBoard_SetText(strCopyString As String) As Boolean
  Dim hGlobalMemory As Long
  Dim lpGlobalMemory As Long
  Dim hClipMemory As Long

  ' Allocate moveable global memory.
  '-------------------------------------------
  hGlobalMemory = GlobalAlloc(GHND, Len(strCopyString) + 1)

  ' Lock the block to get a far pointer
  ' to this memory.
  lpGlobalMemory = GlobalLock(hGlobalMemory)

  ' Copy the string to this global memory.
  lpGlobalMemory = lstrcpy(lpGlobalMemory, strCopyString)

  ' Unlock the memory and then copy to the clipboard
  If GlobalUnlock(hGlobalMemory) = 0 Then
    If OpenClipboard(0&) <> 0 Then
      Call EmptyClipboard
      hClipMemory = SetClipboardData(CF_TEXT, hGlobalMemory)
      ClipBoard_SetText = CBool(CloseClipboard)
    End If
  End If
End Function

Function ClipBoard_GetText() As String
  Dim hClipMemory As Long
  Dim lpClipMemory As Long
  Dim strCBText As String
  Dim RetVal As Long
  Dim lngSize As Long
  If OpenClipboard(0&) <> 0 Then
    ' Obtain the handle to the global memory
    ' block that is referencing the text.
    hClipMemory = GetClipboardData(CF_TEXT)
    If hClipMemory <> 0 Then
      ' Lock Clipboard memory so we can reference
      ' the actual data string.
      lpClipMemory = GlobalLock(hClipMemory)
      If lpClipMemory <> 0 Then
        lngSize = GlobalSize(lpClipMemory)
        strCBText = Space$(lngSize)
        RetVal = lstrcpy(strCBText, lpClipMemory)
        RetVal = GlobalUnlock(hClipMemory)
        ' Peel off the null terminating character.
        strCBText = Left(strCBText, InStr(1, strCBText, Chr$(0), 0) - 1)
      Else
        MsgBox "Could not lock memory to copy string from."
      End If
    End If
    Call CloseClipboard
  End If
  ClipBoard_GetText = strCBText
End Function

Function CopyOlePiccy(Piccy As Object)
  Dim hGlobalMemory As Long, lpGlobalMemory As Long
  Dim hClipMemory As Long, X As Long

  ' Allocate moveable global memory.
  '-------------------------------------------
  hGlobalMemory = GlobalAlloc(GHND, Len(Piccy) + 1)

  ' Lock the block to get a far pointer
  ' to this memory.
  lpGlobalMemory = GlobalLock(hGlobalMemory)


  'Need to copy the object to the memory here

  lpGlobalMemory = lstrcpy(lpGlobalMemory, Piccy)

  ' Unlock the memory.
  If GlobalUnlock(hGlobalMemory) <> 0 Then
    MsgBox "Could not unlock memory location. Copy aborted."
    GoTo OutOfHere2
  End If

  ' Open the Clipboard to copy data to.
  If OpenClipboard(0&) = 0 Then
    MsgBox "Could not open the Clipboard. Copy aborted."
    Exit Function
  End If

  ' Clear the Clipboard.
  X = EmptyClipboard()

  ' Copy the data to the Clipboard.
  hClipMemory = SetClipboardData(CF_TEXT, hGlobalMemory)

OutOfHere2:
  If CloseClipboard() = 0 Then
    MsgBox "Could not close Clipboard."
  End If
End Function
'*********  Code End   ************

