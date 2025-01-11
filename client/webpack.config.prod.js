const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');
const HtmlWebpackPlugin = require('html-webpack-plugin');
const CopyPlugin = require('copy-webpack-plugin');

module.exports = merge(common, {
  mode: 'production',
  plugins: [
    new HtmlWebpackPlugin({
      template: './src/index.html',
    }),
    new CopyPlugin({
      patterns: [
        { from: 'src/img', to: 'img' },
        { from: 'src/css', to: 'css' },
        { from: 'src/js/vendor', to: 'js/vendor' },
        { from: 'src/icon.svg', to: 'icon.svg' },
        { from: 'src/favicon.ico', to: 'favicon.ico' },
        { from: 'src/robots.txt', to: 'robots.txt' },
        { from: 'src/icon.png', to: 'icon.png' },
        { from: 'src/404.html', to: '404.html' },
        { from: 'src/site.webmanifest', to: 'site.webmanifest' },
      ],
    }),
  ],
});
