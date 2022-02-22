"use strict";

module.exports.getRecs = (event, context, callback) => {
  const response = {
    statusCode: 200,
    body: JSON.stringify({
      message: "getRecs executed successfully!",
      input: event,
    }),
  };

  callback(null, response);
};
