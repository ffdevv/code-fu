import { pbkdf2Sync, createCipheriv, createDecipheriv, randomBytes } from "crypto";

const PBKDF_DIGEST_ALGORITHM = 'sha512';
const BINARY_ENCODING = 'base64';
const CIPHER_ALGORITHM = 'aes-256-gcm';
const CIPHER_ALGORITHM_KEY_LENGTH = 32; // bytes
const CIPHER_ALGORITHM_IV_LENGTH = 12; // bytes
const CIPHER_AUTHTAG_LENGTH = 16; // bytes
const SALT_LENGTH = 12; // bytes
const ENCRYPTION_PARAMETERS_SEPARATOR = '$';

export const encrypt = (payload, secret) => {
  const salt = randomBytes(SALT_LENGTH);
  const rounds = 100 + Math.floor(Math.random() * 1000);

  const derived = pbkdf2Sync(secret, salt, rounds, CIPHER_ALGORITHM_KEY_LENGTH, PBKDF_DIGEST_ALGORITHM);
  // NOTE
  // the IV this should be globally unique
  // a bunch of IV reuse (per single derived) in aes-256-gcm can compromise the derived key
  // thus being able to decrypt all the data encrypted with such key
  // it must be 12 bytes (96 bits).
  // salt and rounds randomizing before deriving are intended to dramatically reduce
  // probability to get the same iv with the same derived
  // 2^96 (iv) * 2^96 (salt) * 1000 (rounds) combinations
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

  const authTag = !!CIPHER_AUTHTAG_LENGTH
    ? cipher.getAuthTag().toString(BINARY_ENCODING)
    : ''
    ;

  return {
    ep: [
      rounds.toString(),
      salt.toString(BINARY_ENCODING),
      iv.toString(BINARY_ENCODING),
      authTag
    ].join(ENCRYPTION_PARAMETERS_SEPARATOR),
    data: encrypted.toString(BINARY_ENCODING)
  }
}

export const decrypt = ({ ep, data }, secret) => {
  const epList = ep.split(ENCRYPTION_PARAMETERS_SEPARATOR);
  const r = parseInt(epList[0]);
  const s = Buffer.from(epList[1], BINARY_ENCODING);
  const iv = Buffer.from(epList[2], BINARY_ENCODING);
  let at = epList[3];
  data = Buffer.from(data, BINARY_ENCODING);
  if (at) {
    at = Buffer.from(at, BINARY_ENCODING);
  }
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
