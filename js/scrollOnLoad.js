/*
  Using the sessionStorage make the page automatically scroll to the last position after refreshing
  You can make the scroll position persistent through sessions using the localStorage
  
  usage:
  
  scrollOnLoad();
  scrollOnLoad({getKey: () => window.location.pathname, storage: localStorage});
*/
const ENABLE = true;
const STORAGE = sessionStorage; // localStorage if you want more persistence
const GET_KEY = () => {
  const path = window.location.pathname;
  const search = window.location.search || "";
  return `${path}${search}`;
};
const GET_Y_OFFSET = () => window.pageYOffset;
const BEHAVIOR = "instant"; // "instant" "smooth" "auto"
const SCROLL_RESTORATION = "manual"; // "auto" "manual"

const scrollOnLoad = ({
  storage,
  enable,
  getKey,
  key,
  getYOffset,
  y,
  behavior,
  scrollRestoration
}) => {
  enable ??= ENABLE;
  behavior ??= BEHAVIOR;
  storage ??= STORAGE;
  getKey ??= GET_KEY;
  getYOffset ??= GET_Y_OFFSET;
  scrollRestoration ??= SCROLL_RESTORATION;
  key ??= getKey();

  if (!enable) {
    // enable browser default
    storage.removeItem(key);
    window.history.scrollRestoration = "auto";
    return;
  }

  // set the scroll height in storage
  storage.setItem(key, y ?? storage.getItem(key) ?? getYOffset());
  window.addEventListener(
    "scroll",
    () => storage.setItem(key, y ?? getYOffset()),
    { passive: true }
  );

  // disable auto scroll
  window.history.scrollRestoration = scrollRestoration;

  // custom scroll
  document.onreadystatechange = () => {
    if (document.readyState !== "complete") return;
    window.scroll({
      top: storage.getItem(key) ?? 0,
      behavior: behavior
    });
  };
};

export default scrollOnLoad;
