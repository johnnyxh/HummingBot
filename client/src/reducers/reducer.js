import {
    HEALTH_REQUESTED,
    HEALTH_COMPLETE,
    RESTART_REQUESTED,
    RESTART_COMPLETE
} from '../actions/actions';

export function botReducer(
    state = {
        health: 'Unknown',
        pendingHealth: false,
        pendingRestart: false
    },
    action
) {
    switch (action.type) {
        case HEALTH_COMPLETE:
            return Object.assign({}, state, {
                health: action.payload,
                pendingHealth: false
            });
        case HEALTH_REQUESTED:
            return Object.assign({}, state, {
                pendingHealth: true
            });
        case RESTART_COMPLETE:
            return Object.assign({}, state, {
                pendingRestart: false
            });
        case RESTART_REQUESTED:
            return Object.assign({}, state, {
                pendingRestart: true
            });
        default:
            return state;
    }
};