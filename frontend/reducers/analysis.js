import {AnalysisData} from "../model/analysis";

export function analysis(state = new AnalysisData(), action) {
    switch (action.type) {
        case 'LOAD_STOCK_DATA_SUCCESS':
            return Object.assign({}, state, {
                data: action.stockData,
            });
        case 'RESET_STOCK_DATA':
            return Object.assign({}, state, {
                data: null,
            });
        case 'TOGGLE_WAVELET_ANALYSIS_DETAILS':
            return Object.assign({}, state, {
                showDetails: !state.showDetails,
            });
        case 'TOGGLE_RECOMMENDATIONS':
            return Object.assign({}, state, {
                showRecommendations: !state.showRecommendations,
            });
        default:
            return state;
    }
}