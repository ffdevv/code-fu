const timedFunction = (f) => (...args) => {
  const pre = performance.now();
  f(...args);
  return performance.now() - pre;
}

// how many ms f1 is quickier than f2
const getComparingResults = (f1, f2, opts) => {
  let {commonArgs, f1Args, f2Args, times} = opts || {};
  times ??= 1;
  f1Args ??= commonArgs ?? [];
  f2Args ??= commonArgs ?? [];
  const tf1 = timedFunction(f1);
  const tf2 = timedFunction(f2);
  const results = [];
  for (let i=0; i<times; i++){
    results.push(tf2(...f2Args) - tf1(...f1Args));
  }
  return results;
}

const compare = (...args) => {
  const results = getComparingResults(...args);
  return results.reduce((a,b)=>a+b) / results.length;
}
