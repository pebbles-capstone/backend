"use strict";

const AWS = require("aws-sdk"); // eslint-disable-line import/no-extraneous-dependencies
const uuid = require("uuid");
const dynamoDb = new AWS.DynamoDB.DocumentClient();

function isEmpty(obj) {
  return Object.keys(obj).length === 0;
}
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

module.exports.getUser = (event, context, callback) => {
  try {
    const params = {
      TableName: "UserTable",
      Key: {
        userId: event.path.userId,
      },
    };

    dynamoDb.get(params, (error, result) => {
      if (error || !result.Item || isEmpty(result?.Item)) {
        console.error(error);
        callback(null, {
          statusCode: error?.statusCode || 501,
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
        body: JSON.stringify(result.Item),
      };

      callback(null, response);
    });
  } catch (err) {
    console.error("Failed: " + err.message);
    console.error("Trace: " + err.stack);
    return response(400, { message: err.message });
  }
};

module.exports.updateUser = (event, context, callback) => {
  try {
    if (!event.body) {
      console.error("Validation Failed");
      callback(null, {
        statusCode: 400,
        headers: { "Content-Type": "text/plain" },
        body: "Error no body found",
      });
      return;
    }
    console.log(event.body);
    const data = event.body.body;
    console.log("Data: ", event.body?.body?.user);

    if (typeof data?.user !== "object") {
      console.log(data?.user);
      console.log(typeof data?.user);
      console.error("Validation Failed");
      callback(null, {
        statusCode: 400,
        headers: { "Content-Type": "text/plain" },
        body: "Error putting item",
      });
      return;
    }

    const params = {
      TableName: "UserTable",
      Item: {
        userId: event?.path?.userId || uuid.v1(),
        about: data?.user?.about,
        contact: data?.user?.contact,
        discipline: data?.user?.discipline,
        area: data?.user?.area,
        interests: data?.user?.interests,
        name: data?.user?.name,
        projectCount: data?.user?.projectCount,
        teamID: data?.user?.teamID,
      },
    };

    dynamoDb.put(params, (error) => {
      if (error) {
        console.error(error);
        callback(null, {
          statusCode: error.statusCode || 501,
          headers: { "Content-Type": "text/plain" },
          body: "Error putting item",
        });
        return;
      }
      const response = {
        statusCode: 200,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": true,
        },
        body: JSON.stringify(params),
      };

      callback(null, response);
    });
  } catch (err) {
    console.error("Failed: " + err.message);
    console.error("Trace: " + err.stack);
    return response(400, { message: err.message });
  }
};

module.exports.deleteUser = (event, context, callback) => {
  try {
    const params = {
      TableName: "UserTable",
      Key: {
        userId: event.path.userId,
      },
    };

    dynamoDb.delete(params, (error) => {
      if (error) {
        console.error(error);
        callback(null, {
          statusCode: error.statusCode || 501,
          headers: { "Content-Type": "text/plain" },
          body: "Error Deleting Item.",
        });
        return;
      }

      const response = {
        statusCode: 200,
        headers: {
          "Access-Control-Allow-Origin": "*",
          "Access-Control-Allow-Credentials": true,
        },
        body: JSON.stringify({}),
      };

      callback(null, response);
    });
  } catch (err) {
    console.error("Failed: " + err.message);
    console.error("Trace: " + err.stack);
    return response(400, { message: err.message });
  }
};
