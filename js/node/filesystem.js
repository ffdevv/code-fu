const fs = require('fs');
const { exec } = require("child_process");

const checkFileExists = (fp) => fs.existsSync(fp);
const readFsFileSync = (fp, opts) => fs.readFileSync(fp, opts || {encoding:'utf8', flag:'r'});
const readFile = readFsFileSync; // alias

const readFsStream = (fp) => (
  new Promise((resolve, reject) => {
    const reader = fs.createReadStream(fp);
    let data = "";
    reader
      .on('data', (chunk) => data += chunk.toString())
      .on('end', () => resolve(data))
      .on('error', () => reject())
    ;
  })
);

const readCat = (fp) => (
  new Promise((resolve, reject) => {
    const cmd = `cat ${fp}`;
    exec(cmd, (error, stdout, stderr) => {
      if (error) {
          return resolve(false);
      }
      if (stderr) {
          return resolve(false);
      }
      return resolve(true);
    })
  })
);
