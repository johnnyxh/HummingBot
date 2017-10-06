import {
	HEALTH_UPDATED,
	HEALTH_REQUESTED
} from '../actions/actions';

export function botReducer(
	state = {
		health: 'Unknown',
		pendingHealth: false
	},
	action
) {
	switch(action.type) {
		case HEALTH_UPDATED:
			return Object.assign({}, state, {
				health: action.payload,
				pendingHealth: false
			});
		case HEALTH_REQUESTED:
			return Object.assign({}, state, {
				pendingHealth: true
			});
		default:
			return state;
	}
};