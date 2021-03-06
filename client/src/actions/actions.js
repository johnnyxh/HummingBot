import fetch from 'isomorphic-fetch';

export const HEALTH_REQUESTED = 'HEALTH_REQUESTED';
export const HEALTH_COMPLETE = 'HEALTH_COMPLETE';

export const RESTART_REQUESTED = 'RESTART_REQUESTED';
export const RESTART_COMPLETE = 'RESTART_COMPLETE';

export const PLAYLIST_REQUESTED = 'PLAYLIST_REQUESTED';
export const PLAYLIST_COMPLETE = 'PLAYLIST_COMPLETE';

export const NAVIGATION_CHANGED = 'NAVIGATION_CHANGED';

export function navigationChange(view) {
    return {
        type: NAVIGATION_CHANGED,
        payload: view
    };
};

export function requestHealth() {
    return {
        type: HEALTH_REQUESTED
    };
};

export function requestRestart() {
    return {
        type: RESTART_REQUESTED
    };
};

export function requestPlaylist() {
    return {
        type: PLAYLIST_REQUESTED
    };
};

export function updatePlaylist() {
    return async (dispatch) => {
        dispatch(requestPlaylist());

        const response = await fetch('/api/playlist', {
            method: 'GET',
            headers: {
                Accept: 'application/json'
            }
        });

        if (response.status >= 400) {
            throw new Error('Bad response from server');
        }

        const responseBody = await response.json();

        dispatch({
            type: PLAYLIST_COMPLETE,
            payload: responseBody
        });
    };
};

export function updateHealth() {
    return async (dispatch) => {
        dispatch(requestHealth());

        const response = await fetch('/api/health', {
            method: 'GET',
            headers: {
                Accept: 'application/json'
            }
        });

        if (response.status >= 400) {
            throw new Error('Bad response from server');
        }

        const responseBody = await response.json();

        dispatch({
            type: HEALTH_COMPLETE,
            payload: responseBody
        });
    };
};

export function restartBot() {
    return async (dispatch) => {
        dispatch(requestRestart());

        const response = await fetch('/api/restart', {
            method: 'GET',
            headers: {
                Accept: 'application/json'
            }
        });

        if (response.status >= 400) {
            throw new Error('Bad response from server');
        }

        const responseBody = await response.json();

        dispatch({
            type: RESTART_COMPLETE,
            payload: responseBody
        });
    };
};