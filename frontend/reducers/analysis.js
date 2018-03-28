import {AnalysisData} from "../model/analysis";

export function analysis(state = new AnalysisData(), action) {
    switch (action.type) {
        case 'LOAD_STOCK_DATA_SUCCESS':
            return Object.assign({}, state, {
                data: action.stockData,
            });
        default:
            return state;
    }
}