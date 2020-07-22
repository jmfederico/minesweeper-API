const fs = require("fs");

module.exports = {
  devServer: {
    disableHostCheck: true,
    https: {
      key: fs.readFileSync(process.env.SSL_KEY),
      cert: fs.readFileSync(process.env.SSL_CERT)
    }
  }
};
