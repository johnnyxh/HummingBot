import {
    HEALTH_REQUESTED,
    HEALTH_COMPLETE,
    RESTART_REQUESTED,
    RESTART_COMPLETE,
    NAVIGATION_CHANGED
} from '../actions/actions';

export function botReducer(
    state = {
        status: 'Unknown',
        servers: ['Unknown'],
        uptime: 'Unknown',
        pendingHealth: false,
        pendingRestart: false
    },
    action
) {
    switch (action.type) {
        case HEALTH_COMPLETE:
            return Object.assign({}, state, action.payload, {pendingHealth: false});
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

export function navigationReducer(
    state = {
        currentView: 'Playlist'
    },
    action
) {
    switch (action.type) {
        case NAVIGATION_CHANGED:
            return Object.assign({}, state, {
                currentView: action.payload
            });
        default:
            return state;
    }
};