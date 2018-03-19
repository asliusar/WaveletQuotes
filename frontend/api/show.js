import {checkHttpStatus, parseJSON} from "../lib/utils/utils";

export const showUrl = 'show/';

export function fetchShowsById(id) {
    return fetch('/api/tv/' + id, {
        method: 'get',
        credentials: "same-origin"
    })
    // .then(checkHttpStatus)
        .then((response) => response.text())
        .then(parseJSON)
}


export function updateShowStatusById(id, status, name) {
    return fetch('/api/tvstatus/set', {
        method: 'post',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({tv_id: id, status, tv_name: name}),
        credentials: "same-origin"
    })
    // .then(checkHttpStatus)
        .then((response) => response.text())
        .then(parseJSON)
}


export function updateShowRateById(id, rating, name) {
    return fetch('/api/tvrating/set', {
        method: 'post',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({tv_id: id, rating, tv_name: name}),
        credentials: "same-origin"
    })
    // .then(checkHttpStatus)
        .then((response) => response.text())
        .then(parseJSON)
}

export function updateEpisodeAddById(tv_id, season, episode) {
    return fetch('/api/episode/add', {
        method: 'post',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({tv_id, season, episode}),
        credentials: "same-origin"
    })
        .then((response) => response.text())
        .then(parseJSON)
}


export function updateEpisodeDeleteById(tv_id, season, episode) {
    return fetch('/api/episode/delete', {
        method: 'delete',
        headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({tv_id, season, episode}),
        credentials: "same-origin"
    })
        .then((response) => response.text())
        .then(parseJSON)
}