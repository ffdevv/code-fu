/*
  Persists the state into a sessionStorage location
  The state will persist until the browser session is closed or
  until sessionStorage.clear() or sessionStorage.removeItem(sessionStorageKey)
  are called.
*/
import { useState, useEffect } from "react";

export default function useStateSessionStored(sessionStorageKey, initValue) {
  const [value, setValue] = useState(
    sessionStorage.getItem(sessionStorageKey) || initValue
  );
  
  const free = () => {
    setValue(null);
    sessionStorage.removeItem(sessionStorageKey);
  }
  
  
  useEffect(() => {
    sessionStorage.setItem(sessionStorageKey, value);
  }, [value, sessionStorageKey]);

  return [value, setValue, free];
}
