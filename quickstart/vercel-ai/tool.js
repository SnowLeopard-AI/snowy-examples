const { tool } = require('ai');
const { z } = require('zod');
const { SnowLeopardPlaygroundClient } = require("@snowleopard-ai/client");

// Instantiate your SnowLeopard Client.
// Note! This requires env var SNOWLEOPARD_API_KEY
const snowy = new SnowLeopardPlaygroundClient();

// This is a datafile id that corresponds to a superheroes.db datafile uploaded at https://try.snowleopard.ai
const datafileId = process.env.SNOWLEOPARD_EXAMPLE_DATAFILE_ID;
if (!datafileId) {
  console.error('environment variable SNOWLEOPARD_EXAMPLE_DATAFILE_ID required');
  process.exit(1);
}

// Create a tool for retrieving superhero data
const getData = tool({
  description: 'Retrieve superhero data.\nSuperhero/comic book character database\nContains physical characteristics and publication history',
  inputSchema: z.object({
    userQuestion: z.string().describe('the natural language query to answer'),
  }),
  execute: async ({ userQuestion }) => {
    console.log(`[Tool Call] ${userQuestion}`);
    let resp = await snowy.retrieve(datafileId, userQuestion);
    console.log(`[Tool Response] ${JSON.stringify(resp, null, 2)}`);
    return resp
  }
});

module.exports = { getData };
