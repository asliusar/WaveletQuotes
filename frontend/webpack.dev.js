var webpack = require('webpack');
var path = require('path');
// var autoprefix = require('autoprefixer-core');
// var nested = require('postcss-nested');
// var mixins = require('postcss-mixins');
// var modules = require('postcss-modules');

module.exports = {
    devtool: 'cheap-module-eval-source-map',
    entry: [
        'webpack/hot/dev-server',
        'webpack-hot-middleware/client?__webpack_hmr',
        './'
    ],
    output: {
        path: path.join(__dirname, 'dist'),
        filename: 'bundle.js',
        publicPath: '/',
    },
    resolve: {
        modulesDirectories: ['node_modules'],
        extensions: ['', '.js', '.jsx', '.css'],
    },
    plugins: [
        new webpack.optimize.OccurenceOrderPlugin(),
        new webpack.HotModuleReplacementPlugin(),
        new webpack.NoErrorsPlugin(),
    ],
    module: {
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: /node_modules/,
                loaders: ['babel'],
            },
            {
                test: /\.css$/,
                loaders: [
                    'style',
                    'css-loader?modules&importLoaders=1&localIdentName=[name]__[local]___[hash:base64:5]',
                    'postcss',
                ],
            },
        ],
    },
    // postcss: [
    //   modules({
    //     generateScopedName: '[name]__[local]___[hash:base64:5]',
    //   }),
    //   autoprefix,
    //   mixins,
    //   nested,
    // ],
};
