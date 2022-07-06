const { exec } = require("child_process");

// exec a command redirecting stdout and stderr to the console
consoleExec = (cmd) => {
  return exec(cmd, (error, stdout, stderr) => {
      if (error) {
          console.log(`error: ${error.message}`);
          return;
      }
      if (stderr) {
          console.log(`stderr: ${stderr}`);
          return;
      }
      console.log(`stdout: ${stdout}`);
  });
}
