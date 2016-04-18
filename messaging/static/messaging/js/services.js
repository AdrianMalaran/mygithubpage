var messagingServices = angular.module('messagingServices',['ngWebSocket']);


messagingServices.factory('MessageFactory', ['$http',
	function($http)
	{
		//State variables
		var urlExtensions = 'messaging/message';

		return {
			getContacts:function()
			{
				return $http.get('/chat/get_contacts/');
			},
			switchContacts:function(contactID){
				return $http.get('/chat/get_messages/', {params:{contact_id:contactID}});
			},
			sendMessage:function(message, contact){
				return $http.post('/chat/send_message/', {params:{message:message,contact:contact}});
			},
			getMessages:function()
			{
				console.log('Getting Messages');
			},
			addContact:function()
			{
                return $http.post('/chat/add_contact/', {params:{contact:contact}});	
			}
			
		}
	}]);

//This factory manages the websocket connection for 
//the SMS incoming text messages
messagingServices.factory('WebsocketFactory', ['$http','$websocket',
    function($http,$websocket){
        var websocket=null;
        var missedHeartbeats = 0;
        var heartbeatMessage = '--heartbeat--';
        var trailingMessage = '--messagetrailer--';
        var websocketURI = 'ws://localhost:8000/ws/akalite?subscribe-broadcast';
        var currentWebpage = null;

        return {
                'websocket': websocket,
                'heartbeatMessage': heartbeatMessage,
                'trailingMessage': trailingMessage,
                'currentWebpage': currentWebpage,
                getWebsocket: function() {
                    if(websocket === null){
                        websocket = $websocket(websocketURI);

                        websocket.onOpen(function(){
                            console.log('Websocket Connected!');
                             });

                        websocket.onClose(function(){
                            console.log("Connection closed!");
                            });

                        websocket.onError(function(){
                            console.log("Websocket connection is broken.");
                            });
                        return websocket;
                    }
                    else{
                        return websocket;
                    }
                }
            };
        }
    ]);