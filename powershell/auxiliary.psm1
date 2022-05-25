function NoE {
  Param([string]$s)
  return [String]::IsNullOrEmpty($s)
}

function ConsoleInput {
  Param([string]$s)
  return Read-Host -Prompt $s
}

function ConsoleSecureInput {
  Param([string]$s)
  return Read-Host -AsSecureString -Prompt $s
}

function PSCustomObject2Hashtable {
  Param([PSCustomObject]$o)
  $r = @{}
  $o.PSObject.Properties | ForEach {$r[$_.Name] = $_.Value}
  return $r
}

function HashtablesEq {
  Param(
    [hashtable]$h1,
    [hashtable]$h2
  )
  $ret = $true
  $keys = $h1.Keys + $h2.Keys | Select-Object -Unique 
  foreach ($key in $keys) {
    If (!(($key -in $h1.Keys) -and ($key -in $h2.Keys))){ $ret = $false; break; }
    If ($h1[$key] -ne $h2[$key]){ $ret = $false; break; }
  }
  return $ret
}
