function AES256-Encrypt {
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
        # Check if only Base64Key is provided without Base64IV
        if (($KeyBase64 -xor $KeyBytes) -or ($KeyBytes -xor $IVBytes)) {
            throw "Error: Either provide both Key and IV (or Base64 version) or none of them."
        }
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

        # If Base64Key and Base64IV are provided, use them; otherwise, generate new ones
        if ($KeyBase64 -and $IVBase64) {
            $aes.Key = [Convert]::FromBase64String($KeyBase64)
            $aes.IV  = [Convert]::FromBase64String($IVBase64)
        } elseif ($KeyBytes -and $IVBytes) {
            $aes.Key = $KeyBytes
            $aes.IV  = $IVBytes
        }
        else {
            $aes.GenerateKey()
            $aes.GenerateIV()
        }

        # Encrypt the code
        $encryptor = $aes.CreateEncryptor($aes.Key, $aes.IV)
        $encryptedBytes = $encryptor.TransformFinalBlock($dataBytes, 0, $dataBytes.Length)

        # Create an object to hold the Key, IV, and Encrypted data
        $result = [PSCustomObject]@{
            Key = $aes.Key
            IV = $aes.IV
            Encrypted = $encryptedBytes
        }

        # Output the result object
        $result
    }
}

# Example usage:
# $encrypted = [System.Text.Encoding]::UTF8.GetBytes("Write-Host 'Hello, World!'") | AES256-Encrypt
# $encrypted | Format-List
# [System.Convert]::ToBase64String($encrypted.Key)
# [System.Convert]::ToBase64String($encrypted.IV)
# [System.Convert]::ToBase64String($encrypted.Encrypted)
