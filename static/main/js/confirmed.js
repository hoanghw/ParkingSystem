// JavaScript Document
function confirmed(event){
	var garageName = event.data.garageName;
	var rate = event.data.rate;
	var totalCost = event.data.totalCost;
    var granularity = event.data.granularity;
    var duration = event.data.duration;
	var u = window.localStorage["username"];
    var today = new Date();
    var timestamp = today.getTime();


	$.get(SERVER_URL+"ucheckin/", {data:JSON.stringify({garage:garageName,rate:rate,totalCost:totalCost,username:u,timestamp:timestamp,granularity:granularity,duration:duration})}, function(data, textStatus, jqXHR) {
        },"json")
        .done(function(){
            $('#confirming').modal('hide');
	        $('#content-window').html(changeToParked(garageName));
        })
        .fail(function(){
            $('#confirming').modal('hide');
	        $('#content-window').html(changeToError());
        });
}

function signOut(){
	window.localStorage.removeItem("isLoggedIn");
    window.localStorage.removeItem("username");
    window.localStorage.removeItem("password");
    window.localStorage.removeItem("token");
	window.location.href= "ulogin";
}

function checkOut(){
	$('#content-window').html(changeToNotParked());
}