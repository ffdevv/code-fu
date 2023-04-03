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

const downloadFile = function (fileName, fileContent) {
  var textFile = null,
      makeFile = function (content) {
        var data = new Blob([content], {type: 'text/plain'});
        // If we are replacing a previously generated file we need to
        // manually revoke the object URL to avoid memory leaks.
        if (textFile !== null) {
          window.URL.revokeObjectURL(textFile);
        }
        textFile = window.URL.createObjectURL(data);
        return textFile;
      };

  var link = $("<a></a>");
  link.css('visibility','hidden');
  link.attr("download",fileName);
  link.attr("href", makeFile(fileContent));
  $('body').append(link);
  var e = document.createEvent('MouseEvents');
  e.initEvent( 'click', true, true );
  link[0].dispatchEvent(e);
  link.remove();
};
