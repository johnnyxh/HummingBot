import fetch from 'isomorphic-fetch';

export const HEALTH_UPDATED = 'HEALTH_UPDATED';
export const HEALTH_REQUESTED = 'HEALTH_REQUESTED';

export function requestHealth() {
	return {
		type: HEALTH_REQUESTED
	};
}

export function updateHealth() {
	return async (dispatch) => {
		dispatch(requestHealth());

		// Use this to fetch whatever endpoint will have health
		const response = await fetch('/health');

		dispatch({
			type: HEALTH_UPDATED,
			payload: response.statusText
		});

	}
}