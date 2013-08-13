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