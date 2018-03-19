import 'babel-polyfill';
import React from 'react';
import ReactDOM from 'react-dom';
import {Provider} from 'react-redux';
import configureStore from './lib/index';
import {Router} from 'react-router';
import routes from './routes';
import createBrowserHistory from 'history/lib/createBrowserHistory';
import {browserHistory} from 'react-router';

import injectTapEventPlugin from 'react-tap-event-plugin';
import getMuiTheme from 'material-ui/styles/getMuiTheme';
import MuiThemeProvider from 'material-ui/styles/MuiThemeProvider';

const history = createBrowserHistory();
const store = configureStore(window.__INITIAL_STATE__);

injectTapEventPlugin();

ReactDOM.render(
    <MuiThemeProvider muiTheme={getMuiTheme()}>
        <Provider store={store}>
            <Router children={routes} history={browserHistory}/>
        </Provider>
    </MuiThemeProvider>,
    document.getElementById('react-view'));
