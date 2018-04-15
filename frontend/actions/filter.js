import {fetchStockData} from "../api/analisys";
export function changeStartDate(startDate) {
    return {
        type: 'CHANGE_START_DATE',
        startDate
    }
}

export function changeEndDate(endDate) {
    return {
        type: 'CHANGE_END_DATE',
        endDate
    }
}

export function changeCurrencyPair(pair) {
    return {
        type: 'CHANGE_CURRENCY_PAIR',
        pair
    }
}

export function changeFrequency(frequency) {
    return {
        type: 'CHANGE_FREQUENCY',
        frequency
    }
}

export function resetStockData() {
    return {
        type: 'RESET_STOCK_DATA',
    }
}

// todo develop it
export function loadStockDataFailure() {
    return {}
}

export function loadStockDataSuccess(stockData) {
    return {
        type: 'LOAD_STOCK_DATA_SUCCESS',
        stockData
    }
}
export function loadList() {
    return new Promise((resolve, reject) => {
        resolve(JSON.stringify(
            {}
        ))
    })
}
export function loadStockData(currency, frequency, startDate, endDate) {
    return (dispatch) => {
        resetStockData();
        return fetchStockData(currency, frequency, startDate, endDate)
            .then(stockData => {
                dispatch(loadStockDataSuccess(stockData))
            }).catch(error => {
                loadStockDataFailure(error)
            });
    };
}