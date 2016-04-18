var messagingControllers = angular.module("messagingControllers", ['ui.bootstrap', 'messagingServices' , 'messagingDirectives']);


		// var less = require('less');

		// less.render('.class { width: (1 + 1) }', function (e, output) {
		//   console.log(output.css);
		// });

messagingControllers.controller('messageCtrl', ['$scope', '$http', '$location', 'MessageFactory', 'WebsocketFactory', '$anchorScroll',
	function($scope,$http, $location, MessageFactory, WebsocketFactory, $anchorScroll){
		/////////////////
		////////// Initialization
		/////////////////
		

		$scope.messages = [];
		$scope.contacts = [];

		$scope.select_contact = {
			id:'',
			first_name:'',
			last_name:'',
			phone_number:'',
			messages:''
		}

		$scope.newContact = {
			id:'',
			first:'',
			last:'',
			phone:'',
		}

		$scope.input = { 
			message_field:'',
			time_created:'',
		}

		// $scope.scrollBottom = function(){
		// 	$location.hash('anchor');
		// 	$anchorScroll();
		// }

		$scope.getContacts = function(){
			MessageFactory.getContacts()
			.success(function(data){
				$scope.contacts = [];
				$scope.contacts = data;
				console.log(data);
			})
			.error(function(data){
				console.log("Error retrieving the contacts");
			});
		}
		$scope.getContacts();

		$scope.switchContacts = function(contact){
			$scope.select_contact = contact;
			var contactID = $scope.select_contact.id;

			MessageFactory.switchContacts(contactID)
			.success(function(data){
				$scope.messages = [];
				$scope.messages = data;
			})
			.error(function(){
			})
		}

		$scope.sendMessage=function($event){
			if($event.keyCode == "13" && $scope.input.message_field){

				var contact = angular.toJson($scope.select_contact);
				var message = angular.toJson($scope.input);

				MessageFactory.sendMessage(message,contact)
				.success(function(data){
					console.log("Sent!")
					$scope.messages.push(data);
				})
				.error(function(){
				})
				.finally(function(){
					// $scope.scrollBottom();
				})

				$scope.input.message_field = '';
			}
		}

		WebsocketFactory.getWebsocket();

		WebsocketFactory.getWebsocket().onMessage(function(message){
			newMessage = JSON.parse(message.data);
			$scope.messages.push(newMessage);
			console.log(newMessage);

		})
	}
]);

