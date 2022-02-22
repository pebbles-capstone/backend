"use strict";

module.exports.getProjects = (event, context, callback) => {
  const response = {
    statusCode: 200,
    body: JSON.stringify({
      message: "getProjects executed successfully!",
      input: event,
    }),
  };

  callback(null, response);
};
