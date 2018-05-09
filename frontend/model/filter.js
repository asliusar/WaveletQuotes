export class Filter {
    constructor(initialState) {

        // this.startDate = new Date("2016-11-11");
        this.startDate = new Date("2017-04-11");
        // this.endDate = new Date("2017-10-01");
        this.endDate = new Date("2017-09-29");

        this.currencyPair = 'eurusd=x';
        this.commonCurrencies = ['eurusd=x', 'usdeur=x'];
        this.availableFrequency = ['TIME_SERIES_DAILY'];
        Object.assign(this, initialState);
    }
}