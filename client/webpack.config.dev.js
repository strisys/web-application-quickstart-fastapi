const { merge } = require('webpack-merge');
const common = require('./webpack.common.js');

module.exports = merge(common, {
  mode: 'development',
  devtool: 'source-map',
  devServer: {
    liveReload: true,
    hot: true,
    open: true,
    static: ['./src'],
    port: 3000
  },
});