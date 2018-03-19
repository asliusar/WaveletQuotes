import {ShowList} from '../model/showList';

export function showList(state = new ShowList(), action) {
    switch (action.type) {
        case 'SHOW_LIST_SUCCESS':
            return Object.assign({}, state, {
                list: action.list,
                filterType: action.filterType,
                page: 1
            });
        case 'SHOW_LIST_LOAD_MORE_SUCCESS':
            return Object.assign({}, state, {
                list: state.list.concat(action.list),
                filterType: action.filterType,
                page: action.page
            });
        case 'SHOW_LIST_REQUESTED':
            return Object.assign({}, state, {
                isLoading: true
            });
        case 'SHOW_LIST_FAILURE':
            return Object.assign({}, state, {
                isLoading: false
            });
        default:
            return state;
    }
}