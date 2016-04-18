var messagingDirectives = angular.module('messagingDirectives',['ngWebSocket']);

messagingDirectives.directive('scrollDirective', function () {
  return {
    scope: {
      scrollBottom: "="
    },
    link: function (scope, element) {
      scope.$watchCollection('scrollBottom', function (newValue) {
        if (newValue)
        {
          $('#message-blob').scrollTop($('#message-blob')[5].scrollHeight);
        }
      });
    }
  }
})