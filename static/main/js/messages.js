// JavaScript Document
function changeToParked(garageName){
	var text = '<div class="well well-sm">'
			+'You are currently parking at '
            +'<strong>'
			+garageName
            +'</strong>'
			+'</div>'
			+'<div class="well well-sm">'
			+'<input id="check-out-btn" class="btn btn-danger" type="button" value="Check Out" onclick="checkOut();"/>'
			+'</div>'
			+'<br/>';
	$('html,body').scrollTop(0);
	return text;
}

function changeToNotParked(){
	var text = '<div class="well well-sm"><strong>Please pick a garage on the map</strong></div>';
	$('html,body').scrollTop(0);
	return text;
}

function changeToError(){
    var text = '<div class="well well-sm"><strong>Internet connection error.  Please try again!</strong></div>';
    $('html,body').scrollTop(0);
    return text;
}

function changeToParkFav(garageName){
    var text ='<div class="well well-sm">'
            +'<span class="fav-garage">&#9733;&#9733; </span><span id="garage-name"><strong>'+garageName+'</strong></span><span class="fav-garage"> &#9733;&#9733;</span><br>'
            +'<font color="#3366ff">Current Rate: </font>'
            +'<strong><span id="rate">Fetching</span></strong>'
            +'<hr>'

            +'<form class="form-horizontal">'
            +'<div class="form-group row" id="select-duration">'
            +'<label for="duration" class="col-lg-3 col-md-3 col-sx-6  control-label">Enter Duration: </label>'
            +'<div class="col-lg-3 col-md-3 col-sx-6">'
            +'<input type="number" class="form-control" id="duration-value" value="2" min="0" max="24">'
            +'</div>'
            +'</div>'
            +'<div class="form-group row" id="select-space">'
            +'<label for="space" class="col-lg-3 col-md-3 col-sx-6 control-label">Enter Space # (Optional): </label>'
            +'<div class="col-lg-3 col-md-3 col-sx-6">'
            +'<input type="number" class="form-control" id="space-value" value="0" min="0">'
            +'</div>'
            +'</div>'

            +'</div>'

            +'<div class="well well-sm">'
            +'<input id="park-btn" class="btn btn-primary" type="button" data-toggle="modal" data-target="#confirming" value="Park Here"/>&nbsp &nbsp'
            +'<input onclick="changeGarage();" id="change-garage-btn" type="button" class="btn btn-warning" value="Change Garage"/>&nbsp &nbsp'
            +'<input onclick="toggleFavorite();" id="mark-favorite-btn" type="button" class="btn" value="Mark as favorite"/>'
            +'</div>'
            +'<br/>';
    $('html,body').scrollTop(0);
    return text;

}