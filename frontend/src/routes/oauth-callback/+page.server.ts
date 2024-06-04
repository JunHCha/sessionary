import type { Load } from '@sveltejs/kit';

export const load: Load = async ({ url }) => {
	const code = url.searchParams.get('code');
	const state = url.searchParams.get('state');
	const error = url.searchParams.get('error');

	if (error) {
		return { props: { error } };
	}

	return { props: { code, state } };
};
