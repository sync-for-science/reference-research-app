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

      $.get('/fhir/Practitioner', data)
      .done(function (data) {
        var results = _.map(data.entries, function (entry) {
          return {
            value: entry.resource.name,
            text: entry.resource.name
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
