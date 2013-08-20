// JavaScript Document
function changeToParked(garageName,endTime){
	var text = '<div class="well well-sm">'
			+'You are currently parking at '
            +'<strong>'
			+garageName
            +'</strong>';
    if (endTime){
        text +=' until '
            + formatTime(endTime);
    }

    text +='</div>'
	    //+'<div class="well well-sm">'
		//+'<input id="check-out-btn" class="btn btn-danger" type="button" value="Check Out" onclick="checkOut();"/>'
		//+'</div>'
		+'<br/>';

	$('html,body').scrollTop(0);
	return text;
}
var formatTime = function(unixTimestamp) {
    var dt = new Date(unixTimestamp * 1000);

    var hours = dt.getHours();
    var minutes = dt.getMinutes();
    var ampm;

    if (hours < 12)
     ampm = 'a.m.'
    else
     ampm = 'p.m.'

    if (hours > 12 )
     hours -= 12;

    if (minutes < 10)
     minutes = '0' + minutes;

    return hours + ":" + minutes + ' ' + ampm;
}

function changeToNotParked(){
	var text = '<div class="well well-sm"><strong>Please pick a garage on the map</strong> - by tapping the P icon</div>';
	$('html,body').scrollTop(0);
	return text;
}

function changeToError(){
    var text = '<div class="well well-sm"><strong>Internet connection error.  Please try again!</strong></div>';
    $('html,body').scrollTop(0);
    return text;
}

function changeToParkingGarage(garageName){
    var text ='<div id="parkingInput" class="well well-sm">'
            +'<span class="fav-garage">&#9733;&#9733; </span><span id="garage-name"><strong>'+garageName+'</strong></span><span class="fav-garage"> &#9733;&#9733;</span>'
            +'<br><font color="#3366ff">Current Rate: </font>'
            +'<strong><span id="rate">Fetching</span></strong>'
            +'<br><br>'

            +'<form class="form-horizontal">'
            +'<div class="form-group row" id="select-duration">'
            +'<label for="duration" class="col-lg-2 col-md-3 col-sx-6  control-label">Enter Duration (hour)</label>'
            +'<div class="col-lg-3 col-md-3 col-sx-6">'
            +'<input type="number" class="form-control" id="duration-value" value="2" min="1" max="24">'
            +'</div>'
            +'</div>'
            +'<div class="form-group row" id="select-space">'
            +'<label for="space" class="col-lg-2 col-md-3 col-sx-6 control-label">Enter Space (optional)</label>'
            +'<div class="col-lg-3 col-md-3 col-sx-6">'
            +'<input type="number" class="form-control" id="space-value" value="0" min="0">'
            +'</div>'
            +'</div>'

            +'</div>'

            +'<div class="well well-sm">'
            +'<input id="park-btn" class="btn-darkblue" type="button" data-toggle="modal" data-target="#confirming" value="Park"/>&nbsp'
            +'<input onclick="toggleFavorite();" id="mark-favorite-btn" type="button" class="btn-orange" value="Favorite"/>&nbsp'
            +'<input onclick="changeGarage();" id="change-garage-btn" type="button" class="btn-darkgreen" value="Go Back"/>'
            +'</div>';
    //$('html,body').scrollTop($('#parkingInput').position().top);
    $('html,body').scrollTop(0);
    return text;

}