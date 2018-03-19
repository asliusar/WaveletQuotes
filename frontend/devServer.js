//-------------Create express app-------------
const express = require('express');
const session = require('express-session');
const path = require('path');
const bodyParser = require('body-parser');
const cookieParser = require('cookie-parser');
const logger = require('morgan');

const webpack = require('webpack');
const config = require("./webpack.dev.js");
const compiler = webpack(config);

const defaultUser = 'default';

// Set up the express app
const app = express();

app.use(require('webpack-dev-middleware')(compiler, {
    noInfo: true,
    publicPath: config.output.publicPath,
}));

app.use(require('webpack-hot-middleware')(compiler));

// Log requests to the console
app.use(logger('dev'));

// Must use cookieParser before session
app.use(cookieParser());

// Initialize session
app.use(session({
    secret: 'ssshhhhh',
    saveUninitialized: true,
    resave: true
}));

// Parse incoming requests data
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({extended: false}));

// Engine

app.engine('html', require('ejs').renderFile);
app.set('view engine', 'html');

app.get('*', function (req, res) {
    if (!req.session.user) req.session.user = defaultUser;
    res.sendFile(path.join(__dirname, 'index.html'));
});

//-------------Create server using express app-------------

const http = require('http');

const port = parseInt(process.env.PORT, 10) || 8080;
app.set('port', port);

const server = http.createServer(app);
server.listen(port, function (err) {
    if (!err) {
        console.log('Server listening at port %d', port);
    }
    else {
        console.error('Error starting web-server on port', port, err.toString());
        process.exit(99);
    }
});
