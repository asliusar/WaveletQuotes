import {Filter} from "../model/filter";

export function filter(state = new Filter(), action) {
    switch (action.type) {
        case 'CHANGE_START_DATE':
            return Object.assign({}, state, {
                startDate: action.startDate,
            });
        case 'CHANGE_END_DATE':
            return Object.assign({}, state, {
                startDate: action.endDate,
            });
        case 'CHANGE_CURRENCY_PAIR':
            return Object.assign({}, state, {
                currencyPair: action.currencyPair,
            });
        case 'CHANGE_FREQUENCY':
            return Object.assign({}, state, {
                frequency: action.frequency,
            });
        default:
            return state;
    }
}