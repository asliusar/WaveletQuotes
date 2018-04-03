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
    let array = [];
    let length = data["timestamp"].length;

    for (let i = 0; i < length; i++) {
        let elem = {};
        for (let column in data) {
            if (column == "timestamp") {
                elem["date"] = new Date(data[column][i]);
            } else {
                elem[column] = data[column][i];
            }
        }
        array.push(elem);
    }

    return array;
}

function mergeDataIntoObjects(json) {
    let data = JSON.parse(json);

    data.timeSeries = generateElementsArray(data.timeSeries);
    data.hurstIndex = generateElementsArray(data.hurstIndex);

    return data;
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
            return mergeDataIntoObjects(data);
        }).catch(e => {
            console.log(e)
        });
}