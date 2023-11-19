// karma.conf.js

const karmaCoverage = require('karma-coverage');

module.exports = config => {
  config.set({
    // ... other config options

    coverageReporter: {
      type: karmaCoverage,
      dir: 'coverage/',

      check: {
        global: {
          statements: 75,
          branches: 75,
          functions: 75,
          lines: 75,
        },
      },
    },
  });
};