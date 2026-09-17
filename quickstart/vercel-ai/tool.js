const { tool } = require('ai');
const { z } = require('zod');
const { SnowLeopardClient } = require("@snowleopard-ai/client");

// Instantiate your SnowLeopard Client.
// Note! This requires env var SNOWLEOPARD_API_KEY
const snowy = new SnowLeopardClient();

// This is the id of your Snow Leopard Cloud instance, found on the Connection Info tab at https://cloud.snowleopard.ai
const instanceId = process.env.SNOWLEOPARD_INSTANCE_ID;
if (!instanceId) {
  console.error('environment variable SNOWLEOPARD_INSTANCE_ID required');
  process.exit(1);
}

// Create a tool for retrieving Northwind data
const getData = tool({
  description: 'Retrieve data from "Northwind" dataset with natural language queries.\nThis dataset includes information about orders, product categories, customer demographics, employees, and geographic regions.\nYou can use this data to provide insights into sales performance, customer behavior, shipping efficiency, and supplier contributions.',
  inputSchema: z.object({
    userQuestion: z.string().describe('the natural language query to answer'),
  }),
  execute: async ({ userQuestion }) => {
    console.log(`[Tool Call] ${userQuestion}`);
    let resp = await snowy.retrieve({ userQuery: userQuestion, instanceId: instanceId });
    console.log(`[Tool Response] ${JSON.stringify(resp, null, 2)}`);
    return resp
  }
});

module.exports = { getData };
