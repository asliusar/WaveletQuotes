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

const parseDate = timeParse("%Y-%m-%d");

export function fetchStockData(currency, frequency, startDate, endDate) {
    return fetch("http://localhost:5000/analyse",
        {
            mode: 'no-cors',
            method: 'post',
            headers: {
                'Accept': 'application/json, text/plain, */*',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                "currency": currency,
                "frequency": frequency,
                "startDate": startDate,
                "endDate": endDate
            })
        })
        .then(response => {
            return response.text()
        })
        .then(data => {
            return tsvParse(data, parseData(parseDate))
        });
}