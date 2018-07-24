const path=require('path');
const webpack = require('webpack');
const MiniCssExtractPlugin = require('mini-css-extract-plugin');
const UglifyJsPlugin = require('uglifyjs-webpack-plugin');
const VueLoaderPlugin = require('vue-loader/lib/plugin');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const HtmlWebpackInlineSourcePlugin = require('html-webpack-inline-source-plugin');
const OptimizeCSSAssetsPlugin = require("optimize-css-assets-webpack-plugin");

module.exports = {
    entry : {
        main : __dirname +'/src/main.js'
        ,login : __dirname +'/src/login.js'
    },
    output : {
        filename : 'del/[name].js',
        path : path.join(__dirname,'dist/')
    },
    mode : 'production',
    // devServer : {
    //     contentBase : "./public",
    //     open:true,
    //     historyApiFallback : true,
    //     inline: true
    // },
    module: {
        rules: [
            {
                test: /\.vue$/,
                use: {
                    loader: 'vue-loader'
                },
                exclude: '/node_modules/'
            },
            {
                test: /\.scss$/,
                use: [ MiniCssExtractPlugin.loader,'css-loader','sass-loader']
            },
            {
                test: /\.js$/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: [
                            ['env']
                        ]
                    }
                },
                exclude: '/node_modules/'
            },
            {
                test: /\.css$/,
                use: [
                    MiniCssExtractPlugin.loader,
                    'css-loader'
                  ],
            },
            {
                test:  /\.(gif|jpg|png)\??.*$/,
                use: [
                    {
                        loader: "url-loader"
                    }
                ]
            },
            {
                test: /\.(eot|svg|ttf|woff|woff2)\w*/,
                loader: 'url-loader'
            }
        ]
    },
    plugins:[
        new webpack.ProvidePlugin({
            $:"jquery",
            jQuery:"jquery",
            "window.jQuery":"jquery"
        }),
        new VueLoaderPlugin(),
        new MiniCssExtractPlugin({filename:'del/[name].css'}),
        new UglifyJsPlugin(),
        new HtmlWebpackPlugin({
            filename: 'main.html',
            template :  __dirname +'main.html',
            minify : {
                removeComments : true, //去掉注释
                collapseWhitespace : true, //去掉空行
            },
            inlineSource : '.(js|css)$', //全部内嵌
            chunks : ['main']
        }),
        new HtmlWebpackPlugin({
            filename: 'login.html',
            template :  __dirname +'login.html',
            minify : {
                removeComments : true, //去掉注释
                collapseWhitespace : true, //去掉空行
            },
            inlineSource : '.(js|css)$', //全部内嵌
            chunks : ['login']
        }),
        new HtmlWebpackInlineSourcePlugin()
    ],
    optimization: {
        minimizer: [
          new OptimizeCSSAssetsPlugin({})
        ]
    }
}