// Factories/services
angular.module("lendingFront.services", ["ngResource"]).
    factory('Owner', function ($resource) {
        var Owner = $resource('/api/v1/owners/:ownerId', { ownerId: '@id' });
        Owner.prototype.isNew = function(){
            return (typeof(this.id) === 'undefined');
        }
        return Owner;
    }).
    factory('Business', function($resource){
        var Business = $resource('/api/v1/business/:ownerId', { ownerId: '@id' });
        Business.prototype.isNew = function(){
            return (typeof(this.id) === 'undefined');
        }
        return Business;
    });


// App module
angular.module("lendingFront", ['ngRoute','ngResource', 'ngCookies', 'lendingFront.services']).
    config(function ($routeProvider) {
        $routeProvider
            .when('/', { templateUrl: '/static/views/owner.html', controller: OwnerController })
            .when('/business', { templateUrl: '/static/views/business.html', controller: BusinessController })
            .when('/decision', { templateUrl: '/static/views/decision.html', controller: DecisionController });
});


// Owner Controller: just record the owner info
function OwnerController($scope, $location, Owner) {
    $scope.owner = new Owner();

    $scope.saveOwner = function() {
        $scope.owner.$save(function(owner, headers){
            toastr.success('Owner recorded');
            $location.path('/business');
        });
    };
}

// Business Controller: Record business info and calculate decision
function BusinessController($scope, $location, $cookies, Business) {
    $scope.business = new Business();

    $scope.saveBusiness = function() {
        $scope.business.$save(function(decision, headers){
            toastr.success('Business recorded');
            $cookies.put('amount', decision.amount);
            $cookies.put('status', decision.status);
            $cookies.put('owner', decision.owner);
            $cookies.put('company', decision.company);
            $location.path('/decision');
        });
    };
}

function DecisionController($scope, $cookies) {
    $scope.decision = {};
    $scope.decision.status = $cookies.get('status');
    $scope.decision.amount = $cookies.get('amount');
    $scope.decision.company = $cookies.get('company');
    $scope.decision.owner = $cookies.get('owner');
}


