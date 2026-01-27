/**
 * Agentuity Configuration
 *
 */

import type { AgentuityConfig } from '@agentuity/cli';

export default {
	/**
	 * Workbench (development only)
	 *
	 * Visual UI for testing agents during development. Not included in production builds.
	 * Omit this section to disable. Access at http://localhost:3500/workbench
	 */
	workbench: {
		route: '/workbench',
		headers: {},
	},
} satisfies AgentuityConfig;
