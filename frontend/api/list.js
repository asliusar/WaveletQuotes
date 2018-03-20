// export function fetchPopularShows(page) {
//     return fetch('/api/tv/popular/' + page, {
//         method: 'get',
//         credentials: "same-origin"
//     })
//     // .then(checkHttpStatus)
//         .then((response) => response.text())
//         .then(parseJSON)
// }

export function loadList() {
    return new Promise((resolve, reject) => {
        resolve(JSON.stringify(
            {}
        ))
    })
}
