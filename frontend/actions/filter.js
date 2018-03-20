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