import React from "react";
import {Route, IndexRoute} from "react-router";
import App from "./containers/index/index";
import Flow from "./containers/flow/flow";

export default (
    <Route name="app" component={ App } path="/">
        <IndexRoute component={ Flow }/>
    </Route>
);
