'use strict';

const path = require('path'),
    webpack = require('webpack'),
    HtmlWebpackPlugin = require('html-webpack-plugin'),
    MiniCssExtractPlugin = require('mini-css-extract-plugin');
const { CleanWebpackPlugin } = require('clean-webpack-plugin');
const { VueLoaderPlugin } = require('vue-loader');


module.exports = {
    entry: {
        index: './src/index.js',
        'mcc_control': './src/mcc_control.js',
        'question_cheatsheet': './src/question_cheatsheet.js'
    },

    node: {
        fs: 'empty',
        tiff: 'empty'
    },

    output: {
        filename: './assets/js/[name].bundle.js'
    },

    module: {
        rules: [
            // Plotly Loader
            {
                test: /\.js$/,
                use: [
                    'ify-loader',
                    'transform-loader?plotly.js/tasks/compress_attributes.js',
                ]
            },
            // script-loader with 'env' preset
            {
                test: /\.js$/,
                exclude: file => (
                    /node_modules/.test(file) &&
                    !/\.vue\.js/.test(file)
                ),
                use: {
                    loader: 'babel-loader'
                }
            },
            // html-loader
            {
                test: /\.html$/,
                use: ['html-loader']
            },
            // sass-loader with sourceMap activated
            {
                test: /\.scss$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true
                        }
                    },
                    {
                        loader: 'sass-loader',
                        options: {
                            sourceMap: true
                        }
                    }
                ]
            },
            // css-loader with sourceMap activated
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    {
                        loader: 'css-loader',
                        options: {
                            sourceMap: true
                        }
                    }
                ]
            },
            // file-loader(for images)
            { test: /\.(jpg|png|gif|svg)$/, use: [ { loader: 'file-loader', options: { name: '[name].[ext]', outputPath: './assets/img/' } } ] },
            // file-loader(for fonts)
            { test: /\.(woff|woff2|eot|ttf|otf)$/, use: ['file-loader'] },
            // file-loader(for mp3 files)
            { test: /\.mp3$/, loader: 'file-loader', options: { name: '[name].[ext]'}},
            {
                test: /\.vue$/,
                loader: 'vue-loader'
            },
        ]
    },

    plugins: [
        // cleaning up only 'dist' folder
        new CleanWebpackPlugin(),
        new HtmlWebpackPlugin({
            template: './src/index.html',
            chunks: ['index'],
            filename: 'index.html'
        }),
        new HtmlWebpackPlugin({
            template: './src/mcc_control.html',
            chunks: ['mcc_control'],
            filename: 'mcc_control.html'
        }),
        new HtmlWebpackPlugin({
            template: './src/question_cheatsheet.html',
            chunks: ['question_cheatsheet'],
            filename: 'question_cheatsheet.html'
        }),
        new MiniCssExtractPlugin({
            // Options similar to the same options in webpackOptions.output
            // both options are optional
            filename: './assets/css/[name].css'
        }),
        new VueLoaderPlugin()
    ],

    resolve: {
        extensions: ['.js', '.vue'],
    }
};
