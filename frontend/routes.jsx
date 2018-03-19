import React from 'react';
import {Route, IndexRoute} from 'react-router';
import App from './containers/index/index';
import ShowListContainer from './containers/list/ShowListConstainer';

export default (
    <Route name="app" component={ App } path="/">
        <IndexRoute component={ ShowListContainer }/>
    </Route>
);
