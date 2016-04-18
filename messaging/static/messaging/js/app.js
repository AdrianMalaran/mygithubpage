// the main app
var messagingApp = angular.module('messagingApp', [
    'messagingServices',
    'messagingControllers',
]);

messagingApp.config(['$routeProvider',
    function($routeProvider)
    {
        $routeProvider
            .when('/', {
                templateUrl: '/static/messaging.html',
                controller: 'messagingCtrl',
            })
    }])