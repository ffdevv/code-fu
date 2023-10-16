function AES256-Decrypt {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$false, ValueFromPipeline=$true)]
        [byte[]]$Data,

        [Parameter(Mandatory=$false)]
        [string]$InputFile,

        [Parameter(Mandatory=$false)]
        [string]$KeyBase64,
        [Parameter(Mandatory=$false)]
        [byte[]]$KeyBytes,

        [Parameter(Mandatory=$false)]
        [string]$IVBase64,
        [Parameter(Mandatory=$false)]
        [byte[]]$IVBytes
    )

    begin {
        if (-not ($KeyBase64 -xor $KeyBytes)){
            throw "Error: Either provide Key as Base64 or Bytes."
        }
        if (-not ($IVBase64 -xor $IVBytes)){
            throw "Error: Either provide IV as Base64 or Bytes."
        }
        
        $Key = if ($KeyBytes) { $KeyBytes } else { [System.Convert]::FromBase64String($KeyBase64) }
        $IV  = if ($IVBytes ) { $IVBytes  } else { [System.Convert]::FromBase64String($IVBase64 ) }

        # Create a list to hold data from the pipeline
        $dataList = @()
    }

    process {
        # If data is provided from the pipeline, add it to the dataList
        if ($Data) {
            $dataList += $Data
        }
    }
    
    end {
        # Read code from file or use the code provided via parameter or pipeline
        $dataBytes = if ($dataList.Count -gt 0) {
            $dataList
        } elseif ($InputFile) {
            [System.IO.File]::ReadAllBytes($InputFile)
        } else {
            throw "Error: Either provide data through the pipeline, the Data parameter, or specify an InputFile."
        }

        # Create an AES object
        $aes = [System.Security.Cryptography.Aes]::Create()
        $aes.Mode = [System.Security.Cryptography.CipherMode]::CBC
        $aes.Padding = [System.Security.Cryptography.PaddingMode]::PKCS7
        $aes.KeySize = $Key.Length * 8
        $aes.Key = $Key
        $aes.IV  = $IV

        # Decrypt data
        $result = $aes.CreateDecryptor().TransformFinalBlock($dataBytes, 0, $dataBytes.Length)

        # Output the decrypted string
        $result
    }
}

# Example usage:
# From a file with specified key and IV
# $decrypted = AES256-Decrypt -InputFile "path\to\encrypted\file" -KeyBase64 "yourBase64Key" -IVBase64 "yourBase64IV"

# From pipeline with raw key and IV
# $decrypted = $encryptedData | AES256-Decrypt -Key $rawKey -IV $rawIV

# Print the decrypted string
# Write-Host [System.Text.Encoding]::UTF8.GetString($decrypted)
