import {
    CopilotRuntime,
    OpenAIAdapter,
    copilotRuntimeNextJSAppRouterEndpoint,
} from '@copilotkit/runtime';

import { NextRequest } from 'next/server';


let openAIAdapter = new OpenAIAdapter({model: "gpt-5-mini"});
const runtime = new CopilotRuntime({
    actions: ({properties, url}) => {
        return [
            {
                name: "fetchNameForUserId",
                description: "Fetches user name from the database for a given ID.",
                parameters: [
                    {
                        name: "userId",
                        type: "string",
                        description: "The ID of the user to fetch data for.",
                        required: true,
                    },
                ],
                handler: async ({userId}: {userId: string}) => {
                    return {
                        name: "Darth Doe",
                    };
                },
            },
        ]
    }
});

export const POST = async (req: NextRequest) => {
    const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
        runtime,
        serviceAdapter: openAIAdapter,
        endpoint: '/api/copilotkit',
    });

    return handleRequest(req);
};
