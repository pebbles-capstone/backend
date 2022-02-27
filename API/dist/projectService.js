"use strict";

const AWS = require("aws-sdk"); //eslint-disable-line import/no-extraneous-dependencies

const dynamoDb = new AWS.DynamoDB.DocumentClient();
const params = {
  TableName: "ProjectTable",
};

module.exports.getProjects = (event, context, callback) => {
  dynamoDb.scan(params, (error, result) => {
    if (error) {
      console.error(error);
      callback(null, {
        statusCode: error.statusCode || 501,
        body: "No Projects found",
      });
      return;
    }

    const response = {
      statusCode: 200,
      body: JSON.stringify(result.Items),
    };

    callback(null, response);
  });
};
