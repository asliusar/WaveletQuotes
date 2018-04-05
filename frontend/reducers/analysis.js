import {AnalysisData} from "../model/analysis";

export function analysis(state = new AnalysisData(), action) {
    switch (action.type) {
        case 'LOAD_STOCK_DATA_SUCCESS':
            return Object.assign({}, state, {
                data: action.stockData,
            });
        case 'TOGGLE_WAVELET_ANALYSIS_DETAILS':
            return Object.assign({}, state, {
                showDetails: !state.showDetails,
            });
        default:
            return state;
    }
}