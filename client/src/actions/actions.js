import fetch from 'isomorphic-fetch';
import { getCookie } from '../utils/cookies';

export const USER_REQUESTED = 'USER_REQUESTED';
export const USER_COMPLETE = 'USER_COMPLETE';

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

export function requestUser() {
    return {
        type: USER_REQUESTED
    };
}

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

export function getUserInfo() {
    return async (dispatch) => {
        dispatch(requestUser());

        const response = await fetch('/api/user', {
            method: 'GET',
            headers: {
                Accept: 'application/json'
            },
            credentials: 'same-origin'
        });

        // User is not logged in
        if (response.status === 401) {
            return dispatch({
                type: USER_COMPLETE,
                payload: null
            })
        } else if (response.status >= 400) {
            throw new Error('Bad response from server');
        }

        const responseBody = await response.json();

        dispatch({
            type: USER_COMPLETE,
            payload: responseBody
        });
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

export function restartBot(server) {
    return async (dispatch) => {
        dispatch(requestRestart());

        const response = await fetch('/api/restart', {
            method: 'POST',
            headers: {
                Accept: 'application/json',
                'X-XSRFToken': getCookie('_xsrf')
            },
            body: JSON.stringify({ server: server }),
            credentials: 'same-origin'
        });

        if (response.status === 403) {
            const contentType = response.headers.get('content-type');

            // Tornado unauthorized response, most likely needs to retrieve token
            if (contentType && contentType.includes('text/html')) {
                return window.location.href = '/api/auth';    
            }
            alert('You do not have permission to restart the bot');
        } else if (response.status >= 400) {
            throw new Error('Bad response from server');
        }

        const responseBody = await response.json();

        dispatch({
            type: RESTART_COMPLETE,
            payload: responseBody
        });
    };
};