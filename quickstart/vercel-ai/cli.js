#!/usr/bin/env node

const readline = require('readline');
const { streamText } = require('ai');
const { openai } = require('@ai-sdk/openai');
const { getData } = require('./tool');

// Get model name from CLI args or environment variable
function getModelName() {
  const modelArg = process.argv.find(arg => arg.startsWith('--model='));
  if (modelArg) return modelArg.split('=')[1];
  const idx = process.argv.indexOf('--model');
  if (idx !== -1 && process.argv[idx + 1]) return process.argv[idx + 1];
  return process.env.MODEL_NAME || 'gpt-4o';
}

const MODEL_NAME = getModelName();

// Create readline interface
const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout,
  prompt: '> '
});

// Conversation history
const messages = [];

console.log(`Agent REPL started using model: ${MODEL_NAME}. Type your commands (Ctrl+C to exit)`);
rl.prompt();

// Handle user input
rl.on('line', async (input) => {
  const trimmedInput = input.trim();

  if (trimmedInput) {
    try {
      // Add user message to history
      messages.push({
        role: 'user',
        content: trimmedInput
      });

      // Generate AI response with streaming
      let continueGeneration = true;

      while (continueGeneration) {
        const result = await streamText({
          model: openai(MODEL_NAME),
          messages: messages,
          tools: {
            getData: getData
          }
        });

        // Stream the text output
        let hasText = false;
        for await (const chunk of result.textStream) {
          process.stdout.write(chunk);
          hasText = true;
        }

        // Ensure we're on a new line after streaming
        if (hasText) {
          console.log();
        }

        // Get response and add messages to history
        const response = await result.response;
        if (response.messages && response.messages.length > 0) {
          messages.push(...response.messages);
        }

        // Check if there are tool calls - if not, we're done
        const toolCalls = await result.toolCalls;
        continueGeneration = toolCalls && toolCalls.length > 0;
      }
    } catch (error) {
      console.error('Error:', error.message);
    }
  }

  rl.prompt();
});

// Handle exit
rl.on('close', () => {
  console.log('\nGoodbye!');
  process.exit(0);
});
