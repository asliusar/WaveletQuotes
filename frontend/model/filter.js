export class Filter {
    constructor(initialState) {

        this.endDate = new Date();
        this.startDate = new Date();
        this.startDate.setFullYear(this.endDate.getFullYear() - 14);
        // todo remove it
        this.endDate.setFullYear(this.endDate.getFullYear() - 1);


        this.currencyPair = 'eurusd=x';
        this.commonCurrencies = ['eurusd=x', 'usdeur=x'];
        this.availableFrequency = ['TIME_SERIES_DAILY'];
        Object.assign(this, initialState);
    }
}