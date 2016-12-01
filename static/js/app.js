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
        var Business = $resource('/api/v1/business/:businessId', { businessId: '@id' });
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
function OwnerController($scope, $location, $cookies, Owner) {
    $scope.owner = new Owner();

    $scope.saveOwner = function() {
        $scope.owner.$save(function(owner, headers){
            $cookies.put('owner_id', owner.owner_id);
            $cookies.put('full_name', owner.first_name + " " + owner.last_name);
            toastr.success(owner.message);
            $location.path('/business');
        }, function(error){
            toastr.error(error.statusText);
            console.log(error);
        });
    };
}

// Business Controller: Record business info and calculate decision
function BusinessController($scope, $location, $cookies, Business) {
    $scope.business = new Business();
    $scope.owner_id = $cookies.get('owner_id');
    $scope.full_name = $cookies.get('full_name');

    $scope.saveBusiness = function() {
        $scope.business.owner_id = $scope.owner_id;
        $scope.business.$save(function(decision, headers){
            toastr.success('Business recorded');
            $cookies.put('amount', decision.amount);
            $cookies.put('status', decision.status);
            $cookies.put('owner_id', decision.owner_id);
            $cookies.put('company', decision.company);
            $cookies.put('full_name', decision.full_name);
            $location.path('/decision');
        }, function(error) {
            toastr.error(error.statusText);
            console.log(error);
        });
    };
}

function DecisionController($scope, $cookies) {
    $scope.decision = {};
    $scope.decision.status = $cookies.get('status');
    $scope.decision.amount = $cookies.get('amount');
    $scope.decision.company = $cookies.get('company');
    $scope.decision.owner_id = $cookies.get('owner_id');
    $scope.decision.full_name = $cookies.get('full_name');
}


