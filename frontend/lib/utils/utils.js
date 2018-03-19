export function checkHttpStatus(response) {
    if ((response.status >= 200 && response.status < 300) || response.status == 404) {
        return response
    } else {
        let error = new Error(response.statusText);
        error.response = response;
        throw error
    }
}

export function parseJSON(response) {
    return JSON.parse(response);
}

export const USER_TYPE = {
    ANONYMOUS: 'Anonymous',
    CLIENT: 'Client'
};

export class ShowStatus {
    id;
    name;

    constructor(id, name) {
        this.id = id;
        this.name = name;
    }
}

export const SHOW_STATUS_TYPE = {
    UNSEEN: new ShowStatus(1, "Unseen"),
    IN_PROGRESS: new ShowStatus(2, 'In progress'),
    ON_HOLD: new ShowStatus(3, "On hold"),
    SEEN: new ShowStatus(4, "Seen"),
    WANT_TO_WATCH: new ShowStatus(5, 'Want to watch')
};

export const STATUS_LIST = [SHOW_STATUS_TYPE.UNSEEN, SHOW_STATUS_TYPE.IN_PROGRESS, SHOW_STATUS_TYPE.ON_HOLD,
    SHOW_STATUS_TYPE.SEEN, SHOW_STATUS_TYPE.WANT_TO_WATCH];

export function formatDate(date) {
    return date.split('\-')[0];
}