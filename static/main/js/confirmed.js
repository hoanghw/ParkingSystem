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

	$.get(SERVER_URL+"ucheckin/", {data:JSON.stringify({garage:garageName,rate:rate,totalCost:totalCost,username:u,timestamp:timestamp,granularity:granularity,duration:duration,space:space})}, function(data, textStatus, jqXHR) {
        },"json")
        .done(function(){
            $('#confirming').modal('hide');
	        $('#content-window').html(changeToParked(garageName,null));
        })
        .fail(function(){
            $('#confirming').modal('hide');
	        $('#content-window').html(changeToError());
        });
}

function changeGarage(){
    $("#content-window").html(changeToNotParked());
    //$('html,body').scrollTop($('#favorite').position().top);
    $('html,body').scrollTop(0);
}

function toggleFavorite(){
    if (isFavorite){
        unmarkFavorite(true);
    }else{
        markFavorite(true);
    }
    updateFavorite(favorite);
}
function markFavorite(toServer){
    $("#mark-favorite-btn").attr("class", "btn btn-danger");
    $("#mark-favorite-btn").val("Unfavorite");
    $(".fav-garage").show();
    if (favorite.indexOf(garageName) == -1)
        favorite.push(garageName);
    isFavorite=true;
    if (toServer){
        updateFavToServer(true);
    }
}
function unmarkFavorite(toServer){
    $("#mark-favorite-btn").attr("class", "btn btn-warning");
    $("#mark-favorite-btn").val("Favorite");
    $(".fav-garage").hide();
    var index = favorite.indexOf(garageName);
    if (index != -1)
        favorite.splice(favorite.indexOf(garageName),1);
    isFavorite=false;
    if (toServer){
        updateFavToServer(false);
    }
}
function updateFavToServer(isFavorite){
    console.log("garage: "+garageName+" isFavorite: "+isFavorite);
    $.get(SERVER_URL+"uupdatefav/", {data:JSON.stringify({garage:garageName,isFavorite:isFavorite,username:window.localStorage["username"]})}, function(data, textStatus, jqXHR) {
        },"json")
        .done(function(){

        })
        .fail(function(){

        });
}

function checkOut(){
    window.localStorage.removeItem('parkingRate');
    window.localStorage.removeItem('parkingGarage');
    window.localStorage.removeItem('parkingEndTime');
	$('#content-window').html(changeToNotParked());
}