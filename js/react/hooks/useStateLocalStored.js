/*
  Persists the state into a localStorage location
  The state will persist through multiple browser sessions,
  until localStorage.clear() or localStorage.removeItem(localStorageKey)
  are called.
*/
import { useState, useEffect } from "react";

export default function useStateLocalStored(localStorageKey, initValue) {
  const [value, setValue] = useState(
    localStorage.getItem(localStorageKey) || initValue
  );

  const free = () => {
    setValue(null);
    localStorage.removeItem(localStorageKey);
  }
  
  useEffect(() => {
    localStorage.setItem(localStorageKey, value);
  }, [value, localStorageKey]);

  return [value, setValue, free];
}
