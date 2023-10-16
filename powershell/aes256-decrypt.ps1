function AES256-Decrypt {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$false, ValueFromPipeline=$true)]
        [byte[]]$Data,

        [Parameter(Mandatory=$false)]
        [string]$InputFile,

        [Parameter(Mandatory=$false)]
        [string]$Base64Key,
        [Parameter(Mandatory=$false)]
        [byte[]]$Key,

        [Parameter(Mandatory=$false)]
        [string]$Base64IV,
        [Parameter(Mandatory=$false)]
        [byte[]]$IV
    )

    process {

        if (-not ($Base64Key -xor $Key)){
            throw "Error: Either provide Base64Key or Key."
        }
        if (-not ($Base64IV -xor $IV)){
            throw "Error: Either provide Base64IV or IV."
        }
        
        $Key = if ($Key) { $Key } else { [System.Convert]::FromBase64String($Base64Key) }
        $IV  = if ($IV ) { $IV  } else { [System.Convert]::FromBase64String($Base64IV ) }
        
        # Read data from file or use the data provided via parameter or pipeline
        $dataBytes = if ($InputFile) {
            [System.IO.File]::ReadAllBytes($InputFile)
        } elseif ($Data) {
            $Data
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
        $decryptedString
    }
}

# Example usage:
# From a file with specified key and IV
# $decrypted = AES256-Decrypt -InputFile "path\to\encrypted\file" -Base64Key "yourBase64Key" -Base64IV "yourBase64IV"

# From pipeline with raw key and IV
# $decrypted = $encryptedData | AES256-Decrypt -Key $rawKey -IV $rawIV

# Print the decrypted string
# Write-Host [System.Text.Encoding]::UTF8.GetString($decrypted)
