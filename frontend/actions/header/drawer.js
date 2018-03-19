export function toggleDrawer(open) {
    return (dispatch) => {
        return dispatch({ type: 'TOGGLE_DRAWER', open });
    };
}

export function closeDrawer() {
    return (dispatch) => {
        return dispatch({ type: 'CLOSE_DRAWER' });
    };
}