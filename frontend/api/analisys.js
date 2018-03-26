import {tsvParse} from "d3-dsv";

export function fetchStockData() {
    return fetch("https://rrag.github.io/react-stockcharts/data/MSFT.tsv")
        .then(response => {
            console.log(response);
            return response.text()
        })
        .then(data => resolve(tsvParse(data, parseData(parseDate))));
}