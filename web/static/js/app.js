var app = angular.module('myApp', []);

app.config(['$interpolateProvider', function ($interpolateProvider) {
	$interpolateProvider.startSymbol('{a');
	$interpolateProvider.endSymbol('a}');
    }]);

app.controller('bodyCtrl', function ($scope, $http) {
    $http.get("/listallrecordA")
	    .then(function (response) {
		data = response.data;
		$scope.username = data.username;
		$scope.email = data.email;
	    });
    $scope.server = function () {
	$scope.panel = "server";
	$http.get("/server1")
		.then(function (response) {
		    $scope.servers = response.data;
		    console.log(response.data);
		});
    };
    $scope.database = function () {
	$scope.panel = "database";
	$http.get("/database1")
		.then(function (response) {
		    $scope.databases = response.data;
		    console.log(response.data);
		});
    };
});