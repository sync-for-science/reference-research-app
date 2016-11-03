require('./styles.less');
require('bootstrap/dist/js/npm');
require('selectize');

var _ = require('underscore');

$(function () {
  var $doctor = $('#doctor').selectize({
    'preload': true,
    'load': function (query, callback) {
      var data = {};

      if (query.length) {
        data.name = query;
      }

      $.get('/api/providers', data)
      .done(function (data) {
        var results = _.map(data, function (provider) {
          return {
            value: provider.id,
            text: provider.name,
          };
        });

        callback(results);
      })
      .fail(function () {
        callback();
      });
    }
  });
});
