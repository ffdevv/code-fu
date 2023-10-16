function AES256-Encrypt {
    [CmdletBinding()]
    param (
        [Parameter(Mandatory=$false, ValueFromPipeline=$true)]
        [string]$Data,

        [Parameter(Mandatory=$false)]
        [string]$InputFile,

        [Parameter(Mandatory=$false)]
        [string]$Base64Key,

        [Parameter(Mandatory=$false)]
        [string]$Base64IV
    )

    process {
        # Check if only Base64Key is provided without Base64IV
        if ($Base64Key -xor $Base64IV) {
            throw "Error: Either provide both Base64Key and Base64IV or none of them."
        }

        # Read code from file or use the code provided via parameter or pipeline
        $data = if ($InputFile) {
            Get-Content -Path $InputFile -Raw
        } elseif ($Data) {
            $Data
        } else {
            throw "Error: Either provide data through the pipeline, the Data parameter, or specify an InputFile."
        }

        # Convert the code to a byte array
        $dataBytes = [System.Text.Encoding]::UTF8.GetBytes($data)

        # Create an AES object
        $aes = [System.Security.Cryptography.Aes]::Create()

        # If Base64Key and Base64IV are provided, use them; otherwise, generate new ones
        if ($Base64Key -and $Base64IV) {
            $aes.Key = [Convert]::FromBase64String($Base64Key)
            $aes.IV = [Convert]::FromBase64String($Base64IV)
        } else {
            $aes.GenerateKey()
            $aes.GenerateIV()
        }

        # Encrypt the code
        $encryptor = $aes.CreateEncryptor($aes.Key, $aes.IV)
        $encryptedBytes = $encryptor.TransformFinalBlock($dataBytes, 0, $codeBytes.Length)

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
# $encrypted = "Write-Host 'Hello, World!'" | Encrypt-CodeBlock
# $encrypted | Format-List
# [System.Convert]::ToBase64String($encrypted.Key)
# [System.Convert]::ToBase64String($encrypted.IV)
# [System.Convert]::ToBase64String($encrypted.Encrypted)
