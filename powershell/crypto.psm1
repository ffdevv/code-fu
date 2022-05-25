function HashBytes {
    [OutputType([Byte[]])]
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
    [Byte]$PipedByte,
    [Parameter(
      Position=2,
      Mandatory=$false
    )]
    [string]$Algorithm = 'sha256'
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
    $Hasher = [System.Security.Cryptography.HashAlgorithm]::Create($Algorithm)
    return $Hasher.ComputeHash($_Bytes)
  }
}

function ChecksumAndTimestamp {
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
    [Byte]$PipedByte,
    [String]$Algorithm = 'sha512',
    [Int]$TrimHash = 0,
    [String]$TimestampFormat = 'yyyyMMddHHmmss'
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
    If ($ExecutePipeProcess){
      # Function called with Pipeline
      $dummy = $_Bytes.Add($PipedByte)
    }
  }
  End {
    $hashHex = HashBytes $_Bytes -Algorithm $Algorithm | BytesToHex
    If ($TrimHash -gt 0) {
      $hashHex = $hashHex.Substring($hashHex.Length - $TrimHash)
    }
    $timestamp = Get-Date -Format $TimestampFormat
    return @{
      Checksum=$hashHex;
      Timestamp=$timestamp
    }
  }
}
