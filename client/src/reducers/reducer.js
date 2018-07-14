import {
    USER_REQUESTED,
    USER_COMPLETE,
    HEALTH_REQUESTED,
    HEALTH_COMPLETE,
    RESTART_REQUESTED,
    RESTART_COMPLETE,
    NAVIGATION_CHANGED,
    PLAYLIST_REQUESTED,
    PLAYLIST_COMPLETE
} from '../actions/actions';

export function botReducer(
    state = {
        status: 'Unknown',
        servers: ['Unknown'],
        uptime: 'Unknown',
        currentSong: null,
        songs: [],
        pendingUser: false,
        pendingHealth: false,
        pendingRestart: false,
        pendingPlaylist: false,
        user: null
    },
    action
) {
    switch (action.type) {
        case USER_COMPLETE:
            return Object.assign({}, state, { user: action.payload }, {
                pendingUser: false
            });
        case HEALTH_COMPLETE:
            return Object.assign({}, state, action.payload, {
                pendingHealth: false
            });
        case PLAYLIST_COMPLETE:
            return Object.assign({}, state, action.payload, {
                pendingPlaylist: false
            });
        case RESTART_COMPLETE:
            return Object.assign({}, state, {
                pendingRestart: false
            });
        case USER_REQUESTED:
            return Object.assign({}, state, {
                pendingUser: true
            });
        case HEALTH_REQUESTED:
            return Object.assign({}, state, {
                pendingHealth: true
            });
        case PLAYLIST_REQUESTED:
            return Object.assign({}, state, {
                pendingPlaylist: true
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