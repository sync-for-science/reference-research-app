var webpack = require('webpack')
var path = require('path')

var buildPath = path.resolve(__dirname, 'researchapp', 'static', 'build');
var assetsPath = path.resolve(__dirname, 'assets', 'main.js');

module.exports = {
  devtool: 'eval',
  entry: {
    assets: [assetsPath],
  },
  output: {
    path: buildPath,
    filename: '[name].js',
    publicPath: '/static/build/',
  },
  plugins: [
    new webpack.ProvidePlugin({
      jQuery: 'jquery',
      $: 'jquery',
    }),
  ],
  module: {
    loaders: [
      {
        test: /\.less$/,
        loaders: ['style', 'css', 'less'],
      },
      {
        test: /\.css$/,
        loaders: ['style', 'css'],
      },
      // the url-loader uses DataUrls.
      // the file-loader emits files.
      {test: /\.(woff|woff2)(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=application/font-woff'},
      {test: /\.ttf(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=application/octet-stream'},
      {test: /\.eot(\?v=\d+\.\d+\.\d+)?$/, loader: 'file'},
      {test: /\.svg(\?v=\d+\.\d+\.\d+)?$/, loader: 'url?limit=10000&mimetype=image/svg+xml'},
    ],
  },

  resolve: {
    extensions: ['', '.webpack.js', '.js'],
  },

  node: {
    fs: 'empty' // avoids error messages
  },
};
