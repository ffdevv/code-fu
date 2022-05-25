function Base64ToBytes {
  [OutputType([Byte[]])]
  Param(
    [Parameter(
      Position=0,
      Mandatory=$true,
      ValueFromPipeline=$true
    )]
    [String]$Base64
  )
  Process {
    return [Convert]::FromBase64String($Base64)
  }
}

function Base64ToFile {
  Param(
    [Parameter(
      Position=0,
      Mandatory=$true,
      ValueFromPipeline=$true
    )]
    [String]$Base64,
    [Parameter(
      Position=1,
      Mandatory=$true
    )]
    [String]$FilePath,
    [Bool]$Overwrite = $false
  )
  Process {
    If ((FileExists $FilePath) -and $Overwrite){
      Write-Warning "File $($FilePath) exists. Preventing Overwrite"
      return
    }
    [IO.File]::WriteAllBytes($FilePath, [Convert]::FromBase64String($Base64))
    return
  }
}

function HexToBytes {
  [OutputType([Byte[]])]
  Param(
    [Parameter(
      Position=0,
      Mandatory=$true,
      ValueFromPipeline=$true
    )]
    [String]$Hex
  )
  Process {
    return [byte[]] -split ($Hex -replace '..', '0x$& ')
  }
}

function BytesToBase64 {
  [OutputType([String])]
  Param(
    [Parameter(
      Position=0, 
      Mandatory=$false
    )]
    [Byte[]]$Bytes,
    [Parameter(
      Position=1,
      Mandatory=$false,
      ValueFromPipeline=$true
    )]
    [Byte]$PipedByte
  )
  Begin {
    [System.Collections.ArrayList] $_Bytes = @()
    $ExecutePipeProcess = -not $PSBoundParameters.ContainsKey('Bytes')

    # Function called with -Bytes
    If (-not $ExecutePipeProcess) {
      $_Bytes = $Bytes
    }
  }

  Process {
    if ($ExecutePipeProcess){
      # Function called with Pipeline
      $dummy = $_Bytes.Add($PipedByte)
    }
  }

  End {
    return [System.Convert]::ToBase64String($_Bytes)
  }

}

function BytesToHex {
  [OutputType([String])]
  Param(
    [Parameter(
      Position=0, 
      Mandatory=$false
    )]
    [Byte[]]$Bytes,
    [Parameter(
      Position=1,
      Mandatory=$false,
      ValueFromPipeline=$true
    )]
    [Byte]$PipedByte
  )

  Begin {
    [System.Collections.ArrayList] $a = @()
    $ExecutePipeProcess = -not $PSBoundParameters.ContainsKey('Bytes')

    # Function called with -Bytes
    If (-not $ExecutePipeProcess) {
      foreach($Byte in $Bytes)
      {
        $dummy = $a.Add([System.BitConverter]::ToString($Byte))
      }
    }
  }

  Process {
    if ($ExecutePipeProcess){
      # Function called with Pipeline
      $dummy = $a.Add([System.BitConverter]::ToString($PipedByte))
    }
  }

  End {
    return ($a -join '')
  }
}

function FileToBase64 {
  [OutputType([String])]
  Param(
    [String]$FilePath
  )
  return [System.Convert]::ToBase64String([System.IO.File]::ReadAllBytes($FilePath))
}

function FileToBytes {
  [OutputType([Byte[]])]
  Param(
    [String]$FilePath
  )
  return [System.IO.File]::ReadAllBytes($FilePath)
}
