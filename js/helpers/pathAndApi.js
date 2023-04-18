const joinPaths = (root, suffix) => (
  (root.endsWith("/") ? root.slice(0, root.length - 1) : root)
  + "/" +
  (suffix.startsWith("/") ? suffix.slice(1) : suffix)
)
