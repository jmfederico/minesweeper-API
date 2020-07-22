const fs = require("fs");

module.exports = {
  publicPath: process.env.NODE_ENV === "production" ? "/static/" : "/",
  devServer: {
    host: process.env.HOST,
    https: {
      key: fs.readFileSync(process.env.SSL_KEY),
      cert: fs.readFileSync(process.env.SSL_CERT)
    }
  }
};
