'use strict';

const webpack = require('webpack');
const merge = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
    mode: 'development',
    plugins: [
        new webpack.DefinePlugin({
            'API_URL': JSON.stringify('http://localhost:8081/api/'),
            'WS_URL': JSON.stringify('ws://localhost:8081/api/')
            // 'API_URL': JSON.stringify('http://daphne-at-hera-backend:8002/api/'),
            // 'WS_URL': JSON.stringify('ws://daphne-at-hera-backend:8002/api/')
            // 'API_URL': JSON.stringify('http://localhost/api/'),
            // 'WS_URL': JSON.stringify('ws://localhost/api/')
        })
    ],
    devtool: 'eval-source-map',
    devServer: {
        historyApiFallback: true,
        noInfo: false,
        host: "0.0.0.0",
        port: 8081,
        proxy: {
            '/api': {
                target: 'http://daphne-at-hera-backend:8002/',
                changeOrigin: true,
                ws: true
            },
            '/server': {
                target: 'http://daphne-at-hera-backend:8002/',
                changeOrigin: true,
                ws: true
            },
            '/static': {
                target: 'http://daphne-at-hera-backend:8002/',
                changeOrigin: true,
                ws: true
            },
        }
    },
});
