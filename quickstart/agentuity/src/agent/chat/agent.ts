/**
 * Chat Agent: A conversational agent with message history.
 * Uses Vercel AI SDK's generateText and persists history via thread state.
 */
import {createAgent} from '@agentuity/runtime';
import {s} from '@agentuity/schema';
import {generateText, type ModelMessage} from 'ai';
import {openai} from '@ai-sdk/openai';
import {getData} from "@agent/tools/getData.ts";

// Get model name from environment variable with default
const MODEL_NAME = process.env.MODEL_NAME || 'gpt-5-mini';


const ToolEntrySchema = s.object({
	toolCallId: s.string(),
	toolName: s.string(),
	args: s.any(),
	result: s.any(),
});

type ToolEntry = s.infer<typeof ToolEntrySchema>;

export const AgentInput = s.object({
	message: s.string().describe('The user message to send to the chat'),
});

export const AgentOutput = s.object({
	tools: s.array(ToolEntrySchema).describe('List of tool calls with their results'),
	response: s.string().describe('The assistant response'),
});


const agent = createAgent('chat', {
	description: 'A conversational chat agent with memory',
	handler: async (ctx, { message }) => {
		const messages: ModelMessage[] = (await ctx.thread.state.get('messages')) ?? [{
			role: 'system',
			content: `You are a helpful AI assistant who can retrieve real time data using your tools.
			When users ask data-related questions, use your tools to get the data to answer them.
			After retrieving data that answers user-questions give a 1 or 2 sentence summary of the data and offer a potential follow up question.
			
			Never offer to perform data manipulation services or other capabilities that you do not have tools to perform.`
		}];
		messages.push({ role: 'user', content: message });

		const allToolCalls: ToolEntry[] = [];

		for (let step = 0; step < 10; step++) {
			const result = await generateText({
				model: openai(MODEL_NAME),
				messages: messages,
				tools: {
					getData: getData,
				}
			});

			const response = result.response;
			messages.push(...response.messages);

			for (const toolCall of result.toolCalls) {
				const toolResult = result.toolResults.find(r => r.toolCallId === toolCall.toolCallId);
				allToolCalls.push({
					toolCallId: toolCall.toolCallId,
					toolName: toolCall.toolName,
					args: toolCall.input,
					result: toolResult?.output,
				});
			}

			if (result.toolCalls.length == 0) {
				return {
					tools: allToolCalls,
					response: result.text,
				}
			}
		}
		throw Error("Agent exceeded maximum number of steps")

	},
	schema: {
		input: AgentInput,
		output: AgentOutput,
	},
});

export default agent;
