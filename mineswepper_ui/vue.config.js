const fs = require("fs");

const config = {
  publicPath: process.env.NODE_ENV === "production" ? "/static/" : "/"
};

if (process.env.NODE_ENV === "development") {
  config.devServer = {
    host: process.env.HOST,
    https: {
      key: fs.readFileSync(process.env.SSL_KEY),
      cert: fs.readFileSync(process.env.SSL_CERT)
    }
  };
}

module.exports = config;
