/**
 * URL path parts
 * group 1: protocol
 * group 2: subdomain(s)
 * group 3: second level domain
 * group 4: top level domain
 * group 5: port
 * group 6: resource path
 * group 7: query
*/
export const URL = /^(?:(.*):\/\/)?(?:(.*)\.)*(.+)\.([a-z]+)(?:\:(\d+))?(\/.*)?(?:\?(.*))$/i

/**
 * Standard format for bcrypt hashes
 * group 1: version
 * group 2: cost factor (log saltRounds)
 * group 3: salt
 * group 4: hash
*/
export const BCRYPT_HASH = /^\$(2[ayb])\$(\d{1,2})\$([a-zA-Z0-9./]{22})([a-zA-Z0-9./]{31})$/

/**
 * Standard email format with mandatory top level domain
 * group 1: user
 * group 2: whole domain
   * group 3: bottom level domain(s)
   * group 4: top level domain
*/
export const EMAIL = /^([a-zA-Z0-9.!#$%&’*+/=?^_`{|}~-]+)@(([a-zA-Z0-9-.]+)\.([a-zA-Z0-9-]+))$/

/**
 * Checks if a plaintext password has
 * 1 lowercase character
 * 1 uppercase character
 * 1 special character
 * length of 8+ (last number)
*/
export const PASSWORD_FORMAT_MIXED_SPECIAL = /^(?=.*[A-Z])(?=.*[a-z])(?=.*[^a-zA-Z0-9\s])[^\n]{8,}$/

/**
 * Checks if a username is valid
 * use simple characters only and _ - .
 * length of 3+ (last number)
*/
export const USERNAME_SIMPLE = /^[a-zA-Z0-9_.-]{3,}$/


/**
 * Ip v4 format
 *
*/
export const IPV4 = /(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9]?[0-9])(?=\s|$)/
