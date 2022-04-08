import { pbkdf2Sync, createCipheriv, createDecipheriv, randomBytes } from "crypto";

const PBKDF_DIGEST_ALGORITHM = 'sha512';
const PBKDF_MIN_ROUNDS = 250;
const PBKDF_MAX_ROUNDS = 2250;
const BINARY_ENCODING = 'base64';
const CIPHER_ALGORITHM = 'aes-256-gcm';
const CIPHER_ALGORITHM_KEY_LENGTH = 32; // bytes
const CIPHER_ALGORITHM_IV_LENGTH = 12; // bytes
const CIPHER_AUTHTAG_LENGTH = 16; // bytes
const SALT_LENGTH = 12; // bytes

export const encrypt = (payload, secret) => {
  const salt = randomBytes(SALT_LENGTH);
  const rounds = PBKDF_MIN_ROUNDS + Math.floor(Math.random() * (PBKDF_MAX_ROUNDS - PBKDF_MIN_ROUNDS));

  const derived = pbkdf2Sync(secret, salt, rounds, CIPHER_ALGORITHM_KEY_LENGTH, PBKDF_DIGEST_ALGORITHM);
  // NOTE
  // the IV this should be globally unique
  // a bunch of IV reuse (per single derived) in aes-256-gcm can compromise the derived key
  // thus being able to decrypt all the data encrypted with such key
  // it must be 12 bytes (96 bits).
  // salt and rounds randomizing before deriving are intended to dramatically reduce
  // probability to get the same iv with the same derived
  // 2^96 (iv) * 2^96 (salt) * 2000 (different rounds) combinations
  const iv = randomBytes(CIPHER_ALGORITHM_IV_LENGTH);

  const cipher = createCipheriv(CIPHER_ALGORITHM, derived, iv)
  const encrypted = Buffer.concat([
    cipher.update(
      typeof payload === 'string' || payload instanceof Buffer
        ? payload
        : JSON.stringify(payload)
    ),
    cipher.final()
  ]);

  const authTag = {}
  if (CIPHER_AUTHTAG_LENGTH) {
    authTag.at = cipher.getAuthTag().toString(BINARY_ENCODING);
  }
  return {
    ...authTag,
    s: salt.toString(BINARY_ENCODING),
    r: rounds,
    iv: iv.toString(BINARY_ENCODING),
    data: encrypted.toString(BINARY_ENCODING)
  }
}

export const decrypt = ({ s, r, iv, data, at }, secret) => {
  s = Buffer.from(s, BINARY_ENCODING);
  iv = Buffer.from(iv, BINARY_ENCODING);
  data = Buffer.from(data, BINARY_ENCODING);
  if (at) at = Buffer.from(at, BINARY_ENCODING);
  const derived = pbkdf2Sync(secret, s, r, CIPHER_ALGORITHM_KEY_LENGTH, PBKDF_DIGEST_ALGORITHM);
  const decipher = createDecipheriv(CIPHER_ALGORITHM, derived, iv, {
    authTagLength: CIPHER_AUTHTAG_LENGTH || undefined
  });
  if (at) decipher.setAuthTag(at);
  const decrypted = Buffer.concat([decipher.update(data), decipher.final()]);
  try {
    return JSON.parse(decrypted.toString('utf8'));
  } catch (_) {
    return decrypted;
  }
}
