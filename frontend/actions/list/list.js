import {fetchPopularShows, fetchShowsByName, fetchShowsByGenre} from "../../api/list";

export function showListRequested() {
    return {
        type: 'SHOW_LIST_REQUESTED'
    }
}

export function showListSuccess(response) {
    const {page, results, total_results, total_pages} = response;
    return {
        type: 'SHOW_LIST_SUCCESS',
        page,
        list: results,
        totalPages: total_pages,
        totalResults: total_results
    }
}

export function showListLoadMoreSuccess(response) {
    let result = showListSuccess(response);
    result.type = "SHOW_LIST_LOAD_MORE_SUCCESS";
    return result;
}

export function showListFailure() {
    return {
        type: 'POPULAR_SHOW_LIST_FAILURE'
    }
}

export function fetchShowsByFilter(filter, page) {
    debugger;
    return (dispatch) => {
        dispatch(showListRequested());
        return fetchShowsMediator(filter, page)
            .then(response => {
                if (response.page == 1) {
                    window.scrollTo(0, 0);
                    dispatch(showListSuccess(response))
                } else {
                    dispatch(showListLoadMoreSuccess(response));
                }
            }).catch(error => {
                showListFailure(error)
            });
    };

    function fetchShowsMediator(filter, page) {
        page = page == undefined ? 1: page;
        if (filter.genreId != null && filter.genreId != '') {
            return fetchShowsByGenre(filter.genreId, page);
        } else if (filter.name != null && filter.name != '') {
            return fetchShowsByName(filter.name, page);
        } else {
            return fetchPopularShows(page);
        }
    }
}