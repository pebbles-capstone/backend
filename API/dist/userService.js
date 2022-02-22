"use strict";

module.exports.getUser = (event, context, callback) => {
  const response = {
    statusCode: 200,
    body: JSON.stringify({
      message: "getUser function executed successfully!",
      input: event,
    }),
  };

  callback(null, response);
};

module.exports.updateUser = (event, context, callback) => {
  const response = {
    statusCode: 200,
    body: JSON.stringify({
      message: "updateUser function executed successfully!",
      input: event,
    }),
  };

  callback(null, response);
};

module.exports.deleteUser = (event, context, callback) => {
  const response = {
    statusCode: 200,
    body: JSON.stringify({
      message: "deleteUser function executed successfully!",
      input: event,
    }),
  };

  callback(null, response);
};
