'use strict';

const webpack = require('webpack');
const merge = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
    mode: 'production',
    plugins: [
        new webpack.DefinePlugin({
            'API_URL': JSON.stringify('https://daphne-at.selva-research.com/api/'),
            'WS_URL': JSON.stringify('wss://daphne-at.selva-research.com/api/')
        })
    ],
    devServer: {
        historyApiFallback: true,
        noInfo: false,
        proxy: {
            '/api': {
                target: 'https://daphne-at.selva-research.com/',
                changeOrigin: true,
                ws: true
            },
            '/static': {
                target: 'https://daphne-at.selva-research.com/',
                changeOrigin: true,
                ws: true
            }
        }
    },
});
