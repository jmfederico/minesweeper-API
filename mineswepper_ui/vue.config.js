const fs = require("fs");

module.exports = {
  devServer: {
    host: process.env.HOST,
    https: {
      key: fs.readFileSync(process.env.SSL_KEY),
      cert: fs.readFileSync(process.env.SSL_CERT)
    }
  }
};
