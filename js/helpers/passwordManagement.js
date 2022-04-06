/**

  Utilities for password management / encryption / decryption

*/

import { hash, hashSync, compare, compareSync } from 'bcrypt';
import { performance } from "perf_hooks"

const SALT_ROUNDS = null;
const AUTO_ADJOUST_DIFFICULTY_TO_MS = 1500;
const VALIDATION_RX = /^(?=.*[A-Z])(?=.*[a-z])(?=.*[^a-zA-Z0-9\s])[^\n]{8,}$/;
const VALIDATION_DESCRIPTION = "Password must contains: at least 1 uppercase character, 1 lowercase character, 1 special character, and length >= 8";

/***
  * compute the saltRounds needed to get close to the target
  * @param {Number} target milliseconds required for hashing a password
*/
export function getDifficulty(target) {
  const plainTextPassword = "DkepE_oe:.`^??*asd";
  let start, lambdas = [], saltRounds = 1;
  while (true) {
    start = performance.now();
    hashSync(plainTextPassword, saltRounds);
    lambdas.push(performance.now() - start);
    if (lambdas[lambdas.length - 1] > target) break;
    saltRounds++;
  }
  if (lambdas.length === 1) return saltRounds;
  if (
    (target - lambdas[lambdas.length - 2]) <
    (lambdas[lambdas.length - 1] - target)
  ) { return saltRounds - 1; }
  return saltRounds;
}

export default function configurePasswordManagement({
  saltRounds,
  autoAdjoustDifficultyToMs,
  validationRx,
  validationDescription
}) {
  validationRx ||= VALIDATION_RX;
  validationDescription ||= validationRx === VALIDATION_RX ? VALIDATION_DESCRIPTION : "Invalid password";
  saltRounds ||= SALT_ROUNDS;
  if (!saltRounds) {
    autoAdjoustDifficultyToMs ||= AUTO_ADJOUST_DIFFICULTY_TO_MS;
    if (!autoAdjoustDifficultyToMs) {
      throw new Error(
        "AUTO_ADJOUST_DIFFICULTY_TO_MS should be set as numeric fallback"
      )
    }
    saltRounds = getDifficulty(autoAdjoustDifficultyToMs);
  }

  const validatePassword = (plainText, callback) => {
    if (callback && typeof callback === 'function') {
      return validationRx.match(plainText)
        ? callback(null, true)
        : callback(validationDescription, false)
        ;
    }
    return Promise((resolve, reject) => {
      if (validationRx.match(plainText)) return resolve(true);
      reject(validationDescription);
    })
  }
  const validatePasswordSync = (plainText) => !!validationRx.match(plainText);
  const hashPassword = (plainText, callback) => hash(plainText, saltRounds, callback);
  const hashPasswordSync = (plainText) => hashSync(plainText, saltRounds);
  const checkPassword = (plainText, hash, callback) => compare(plainText, hash, callback);
  const checkPasswordSync = (plainText, hash) => compareSync(plainText, hash);

  return {
    hashPassword,
    hashPasswordSync,
    checkPassword,
    checkPasswordSync,
    validatePassword,
    validatePasswordSync,
    validationDescription,
    saltRounds
  }
}
