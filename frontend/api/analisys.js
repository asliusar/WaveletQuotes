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

export function fetchStockData() {
    return fetch("https://rrag.github.io/react-stockcharts/data/MSFT.tsv")
        .then(response => {
            console.log(response);
            return response.text()
        })
        .then(data => {
            console.log(11);
            return tsvParse(data, parseData(parseDate))
        });
}