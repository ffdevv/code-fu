const downloadAsBlob = async (
  url,
  fetchOpts = { credentials: "same-origin" }
) => {
  return await fetch(url, fetchOpts).then((response) => response.blob());
};

const blobToB64 = async (blob, trimMetadata = true) => {
  let result = await new Promise((resolve) => {
    let reader = new FileReader();
    reader.onload = (e) => resolve(reader.result);
    reader.readAsDataURL(blob);
  });

  return trimMetadata ? result.substr(result.indexOf(",") + 1) : result;
};
