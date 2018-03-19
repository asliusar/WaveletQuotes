export class Filter {
    constructor(initialState) {
        this.startDate = new Date();
        this.endDate = new Date();
        this.currencyPair = 'eurusd=x';
        this.commonCurrencies = ['eurusd=x', 'usdeur=x'];
        this.availableFrequency = ['TIME_SERIES_DAILY'];
        Object.assign(this, initialState);
    }
}