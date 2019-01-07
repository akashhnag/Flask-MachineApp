angular.module('myApp', [])
    .controller('HomeCtrl', function($scope, $http, $window) {

        $scope.info = {};
        $scope.showAdd = true;        
        $scope.data;
        $scope.machineIndex;

        //getting Machine details
        $http.get('http://127.0.0.1:8080/machineDetails').then((res)=>{
            console.log('get response',res); 
            $scope.data=res.data;           
        },err=>console.log(err))

        //for adding machine
        $scope.addMachine = function() {
            console.log($scope.info);
            let data= {
                info: $scope.info
            }
            console.log('data',data);
            
            $http.post('http://127.0.0.1:8080/addMachine',data).then((res)=>{
                console.log('response from server ',res);
                $window.location.reload();
                
            },err=>console.log(err))
        }

        //update index
        $scope.updateIndex= function(ind){
            $scope.machineIndex=ind;
            console.log(ind);            
        }

        //for deleting machine
        $scope.delete=function(dat){
            console.log('to be deleted',dat);
            let data={data:dat}
            console.log(data);
            
            $http.post('http://127.0.0.1:8080/deleteMachine',data).then((res)=>{
                console.log(res.data);
                $window.location.reload();
                
            },err=>console.log(err))
        }

        //for updating machine
        $scope.updateMachine = function(){          
            console.log('Edit info',$scope.info);
            console.log(Object.keys($scope.info));
            console.log('Machine name',$scope.data[$scope.machineIndex].device);        

            let data={device:$scope.data[$scope.machineIndex].device,
                        edit:$scope.info
                    }
            $http.put('http://127.0.0.1:8080/updateMachine',data).then((res)=>{
                console.log(res.data);
                $window.location.reload();
            },err=>{
                console.log('Updation Error');
                
            })
            
        }        

    })
