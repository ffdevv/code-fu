export const max = (arr) => arr.reduce((acc,itm) => itm > acc ? itm : acc);
export const mathMax = (arr) => Math.max(...arr);
export const min = (arr) => arr.reduce((acc,itm) => itm < acc ? itm : acc);
export const mathMin = (arr) => Math.min(...arr);
export const sum = (arr) => arr.reduce((acc,itm) => acc + itm);

export const isInt = Number.isInteger;
export const isNumber = Number.isFinite; // will return false on NaN, null, undefined, Infinity, -Infinity

export const toInt = Math.floor;

/***
/** 
  mcm (lcm) MCD (gcd) and common divisors
*/
export const commonDivisors = (a, b) => {
  if (!(
    Number.isInteger(a) && 
    Number.isInteger(b)
  )) throw new Error("Numbers must be integer");
  const ret = [1];
  const lowest = Math.min(a, b);
  for (let i=2; i <= lowest; i++){
    if (!(a%i) && !(b%i)) ret.push(i);
  }
  return ret;
}

// export const gcd = (a, b) => max(commonDivisors(a,b)); // can be slow
export const gcd = (a, b) => b ? gcd(b, a % b) : a;
export const greatestCommonDivisor = gcd;

export const lcm = (a, b) => toInt(a * b / gcd(a,b));
export const leastCommonMultiple = lcm

/***
/** 
  FRACTIONS
  
*/

export const fractionIsInt = ([n, d]) => !(n%d);

export const fractionToInt = ([n, d]) => {
  if (n%d) throw new Error("ValueError: cannot be reduced to an int");
  return toInt(n/d);
}

export const reduceFraction = ([n, d]) => {
  cd = commonDivisors(n, d);
  while (cd.length > 1){
    n /= cd[cd.length-1];
    d /= cd[cd.length-1];
    cd = commonDivisors(n, d)
  }
  return [n, d];
}

export const sumTwoFractions = ([n1, d1], [n2, d2], useLcm = true) => {
  if (!useLcm) {
    return [n1*d2 + n2*d1, d1*d2];
  }
  const d = lcm(d1, d2);
  const n = (d / d1 * n1) + (d / d2 * n2);
  return [n, d];
}

export const sumFractions = (...args) => args.reduce((acc, itm) => sumTwoFractions(acc, itm, true), [0,1]);
