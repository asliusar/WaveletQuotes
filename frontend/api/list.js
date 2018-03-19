import {checkHttpStatus, parseJSON} from "../lib/utils/utils";

export function fetchPopularShows(page) {
    return fetch('/api/tv/popular/' + page, {
        method: 'get',
        credentials: "same-origin"
    })
    // .then(checkHttpStatus)
        .then((response) => response.text())
        .then(parseJSON)
}

export function fetchShowsByName(name, page) {
    return fetch('/api/tv/searchByName/' + name + '/' + page, {
        method: 'get',
        credentials: "same-origin"
    })
    // .then(checkHttpStatus)
        .then((response) => response.text())
        .then(parseJSON)
}

export function fetchShowsByGenre(genre, page) {
    return fetch('/api/tv/searchByGenres/' + genre + '/' + page, {
        method: 'get',
        credentials: "same-origin"
    })
    // .then(checkHttpStatus)
        .then((response) => response.text())
        .then(parseJSON)
}