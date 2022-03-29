/*
  Persists the state into a localStorage location
*/
import { useState, useEffect } from "react";

export default function useStateLocallyStored(localStorageKey, initValue) {
  const [value, setValue] = useState(
    localStorage.getItem(localStorageKey) || initValue
  );

  useEffect(() => {
    localStorage.setItem(localStorageKey, value);
  }, [value, localStorageKey]);

  return [value, setValue];
}
