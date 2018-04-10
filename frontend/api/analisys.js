import {timeParse} from "d3-time-format";

function modifyTime(data) {
    for (let elem of data) {
        elem.date = new Date(elem.date)
    }

    return data;
}

function preprocessing(json) {
    let data = JSON.parse(json);

    data.timeSeries = modifyTime(data.timeSeries);

    return data;
}

export function checkHttpStatus(response) {
    if ((response.status >= 200 && response.status < 300) || response.status == 404) {
        return response
    } else {
        let error = new Error(response.statusText);
        error.response = response;
        throw error
    }
}

export function fetchStockData(currency, frequency, startDate, endDate) {
    return fetch("http://localhost:5000/analyse",
        {
            method: 'post',
            timeout: 10000,
            headers: {
                credentials: "same-origin"
            },
            dataType: 'json',
            body: JSON.stringify({
                "currency": currency,
                "frequency": frequency,
                "startDate": startDate,
                "endDate": endDate
            })
        })
        .then(response => {
            return response.json();
        })
        .then(data => {
            return preprocessing(data);
        }).catch(e => {
            console.log(e)
        });
}