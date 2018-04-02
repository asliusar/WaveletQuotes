import {tsvParse} from "d3-dsv";
import {timeParse} from "d3-time-format";

function parseData(parse) {
    return function (d) {
        d.date = parse(d.date);
        d.open = +d.open;
        d.high = +d.high;
        d.low = +d.low;
        d.close = +d.close;
        d.volume = +d.volume;

        return d;
    };
}

function generateElementsArray(data) {
    for in
}

function mergeDataIntoObjects(json) {
    let data = JSON.parse(json);

    let stockData = generateElementsArray(data.timeSeries);
    let hurstIndex = generateElementsArray(data.hurstIndex);
}

const parseDate = timeParse("%Y-%m-%d");

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
            return tsvParse(data, parseData(parseDate));
        }).catch(e => {
            console.log(e)
        });
}