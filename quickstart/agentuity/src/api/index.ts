import { createRouter } from '@agentuity/runtime';
import chat from '../agent/chat/agent';

const api = createRouter();

// conversation turn with your agent
api.post('/chat', chat.validator(), async (c) => {
	const data = c.req.valid('json');
	return c.json(await chat.run(data));
});

// an empty endpoint makes thread management easier to bootstrap
api.post('/chat/init', async (c) => {
	return c.json({ status: 'done' });
});

export default api;
