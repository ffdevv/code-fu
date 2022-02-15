'''
'    Paste coordinates into cels
'    Copyright (C) 2022 Federico Fogo
'
'    This program is free software: you can redistribute it and/or modify
'    it under the terms of the GNU General Public License as published by
'    the Free Software Foundation, either version 3 of the License, or
'    (at your option) any later version.
'
'    This program is distributed in the hope that it will be useful,
'    but WITHOUT ANY WARRANTY; without even the implied warranty of
'    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
'    GNU General Public License for more details.
'
'    You should have received a copy of the GNU General Public License
'    along with this program.  If not, see https://www.gnu.org/licenses/lgpl-3.0.html
'''

Sub pasteCoordsCH03()
  ' Need Tools/Reference to C:\Windows\System32\FM20.dll
  ' aka Microsoft Forms 2.0 Object Library
 
  Dim RX_PATTERN as String
  Dim COORD_N_COL_NUMBER as Integer
  Dim COORD_E_COL_NUMBER as Integer
  ' Must capture 2 groups for (coord_n) (coord_e)
  ' eg: (600000.123)456, (200000.123)456
  RX_PATTERN = "(\d{6}\.{0,1}\d{0,3})\d*,\s(\d{6}\.{0,1}\d{0,3})\d*"
  COORD_N_COL_NUMBER = 2
  COORD_E_COL_NUMBER = 3
  
  Dim objData As MSForms.DataObject
  Set objData = New MSForms.DataObject
  objData.GetFromClipboard

  strPaste = objData.GetText(1)
  If strPaste = False OR strPaste = "" Then 
    Set objData = Nothing
    Exit Sub
  End If

  Dim rxpExp As Object
  Set rxpExp = CreateObject("VBScript.RegExp")
  rxpExp.Pattern = RX_PATTERN

  If rxpExp.Test(strPaste) = True Then
    Set matchFirst = rxpExp.Execute(strPaste).Item(0)
    Cells(ActiveCell.Row, COORD_N_COL_NUMBER).Value = matchFirst.SubMatches.Item(0)
    Cells(ActiveCell.Row, COORD_E_COL_NUMBER).Value = matchFirst.SubMatches.Item(1)
  End If

  Set objData = Nothing
End Sub
