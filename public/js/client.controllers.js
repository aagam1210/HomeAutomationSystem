/** 
 * Client side - angularJS - where controllers are defined.
 * HTML talks to these controllers.
 */

var homeControllers = angular.module('HomeControllers', []);

homeControllers.controller('HomeController', ['$scope', '$rootScope', '$http', '$interval', 
function ($scope, $rootScope, $http, $interval) {

  $scope.changeStatus = function(id){
    console.log($("#switch" + id).prop('checked'));

    if (($("#switch" + id).prop('checked')) == false) {
      command = "ON " + id;
    }
    else{
      command = "OFF " + id;
    }
    $http.post('/changeswitch',
      { data: command }).then(function successCallback(response){
        alert("status changed");
        }, function errorCallback(response){
          console.log("failed to change applicance state");
          });
  };
 
   // Set of all tasks that should be performed periodically
  var runIntervalTasks = function() {
    $http({
      method: 'GET',
      url: '/sensordata'
    }).then(function successCallback(response) {
      // console.log(response.data.payload);
      if (response.data.payload !== undefined) {
        // switch on when motion is detected
        var payload = response.data.payload;
        if(payload['Light Status 1'] == "OFF"){
            $('#switch1').prop('checked', false);
          }
        else{
            $('#switch1').prop('checked', true);
        }
        if(payload['Light Status 2'] == "OFF"){
            $('#switch2').prop('checked', false);
          }
        else{
            $('#switch2').prop('checked', true);
        }
        if(payload['Light Status 3'] == "OFF"){
            $('#switch3').prop('checked', false);
          }
        else{
            $('#switch3').prop('checked', true);
        }
      }
    }, function errorCallback(response) {
        console.log("failed to listen to sensor data");
    });   
  };


  var polling;
  var startPolling = function(pollingInterval) {
    polling = $interval(function() {
      runIntervalTasks();
    }, pollingInterval);
  };

  var stopPolling = function() {
    // console.log("stop polling");
    if (angular.isDefined(polling)) {
      $interval.cancel(polling);
      polling = undefined;
    }
  };
  // Someone asked us to refresh
  $rootScope.$on('refreshSensorData', function(){
    // Check for new input events twice per second
    // console.log("polling");
    var pollingInterval = 500;
    // Prevent race conditions - stop any current polling, then issue a new
    // refresh task immediately, and then start polling.  Note that polling
    // sleeps first, so we won't be running two refreshes back-to-back.
    stopPolling();
    runIntervalTasks();
    startPolling(pollingInterval);
  });

  // Tell ourselves to refresh new mail count and start polling
  $rootScope.$broadcast('refreshSensorData');
  $scope.$on('$destroy', function() {
    stopPolling();
  });
}
]);

