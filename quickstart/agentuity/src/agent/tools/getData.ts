import {tool} from "ai";
import {z} from "zod";
import {SnowLeopardClient} from "@snowleopard-ai/client";


const datafileId = process.env.SNOWLEOPARD_DATAFILE_ID!;
if (!datafileId) { throw new Error("SNOWLEOPARD_DATAFILE_ID environment variable is required"); }
const snowLeopardToken = process.env.SNOWLEOPARD_API_KEY!;
if (!snowLeopardToken) { throw new Error("SNOWLEOPARD_API_KEY environment variable is required"); }
const snowy = new SnowLeopardClient({ apiKey: snowLeopardToken });

export const getData = tool({
    description:
        'Retrieve data from "Northwind" dataset with natural language queries.\nThis dataset includes information about orders, product categories, customer demographics, employees, and geographic regions.\nYou can use this data to provide insights into sales performance, customer behavior, shipping efficiency, and supplier contributions.',
    inputSchema: z.object({
        userQuestion: z.string().describe('the natural language query to answer'),
    }),
    execute: async ({userQuestion}) => {
        console.log(`[Tool Call] ${userQuestion}`);
        const resp = await snowy.retrieve({userQuery: userQuestion, datafileId: datafileId!});
        console.log(`[Tool Response] ${JSON.stringify(resp, null, 2)}`);
        return resp;
    },
});
