"use strict";

const AWS = require("aws-sdk"); // eslint-disable-line import/no-extraneous-dependencies
const uuid = require("uuid");
const dynamoDb = new AWS.DynamoDB.DocumentClient();

// response helper
const response = (statusCode, body, additionalHeaders) => ({
  statusCode,
  body: JSON.stringify(body),
  headers: {
    "Content-Type": "application/json",
    "Access-Control-Allow-Origin": "*",
    ...additionalHeaders,
  },
});
module.exports.getRecs = (event, context, callback) => {
  try {
    const params = {
      TableName: "RecsTable",
      Key: {
        userId: event.pathParameters.id,
      },
    };

    dynamoDb.getItem(params, (error, result) => {
      if (error) {
        console.error(error);
        callback(null, {
          statusCode: error.statusCode || 501,
          body: "No User found",
        });
        return;
      }

      const response = {
        statusCode: 200,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": true,
        },
        body: JSON.stringify(result.Items),
      };

      callback(null, response);
    });
  } catch (err) {
    console.error("Failed: " + err.message);
    console.error("Trace: " + err.stack);
    return response(400, { message: err.message });
  }
};
