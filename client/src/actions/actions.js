import fetch from 'isomorphic-fetch';

export const HEALTH_REQUESTED = 'HEALTH_REQUESTED';
export const HEALTH_COMPLETE = 'HEALTH_COMPLETE';

export const RESTART_REQUESTED = 'RESTART_REQUESTED';
export const RESTART_COMPLETE = 'RESTART_COMPLETE';

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

export function updateHealth() {
    return async(dispatch) => {
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
            payload: responseBody.status
        });
    };
};

export function restartBot() {
    return async(dispatch) => {
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
            payload: responseBody.status
        });
    };
};