var homeControllers = angular.module("homeController",['ui.bootstrap']);

homeControllers.controller('homeCtrl', ['$scope', '$http',
 function($scope, $http){

 	$scope.contact = function(){

 		$scope.contact = {
 			name: '',
 			email: '',
 			message: '',
 		}

 		http.post('/chat/get_messages/', {params:{name:name, email:email,message:message}})
 		.success(function(){
 			console.log("Message Sent");
 		})
 		.error(function(){
 			console.log("Error");
 		})
 		.finally(function(){

 		})
 	}

}])