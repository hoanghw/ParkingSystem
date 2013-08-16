// JavaScript Document
var width = $(window).width();
var height = $(window).height();
var garageName="default";
var rate=17;
var totalCost=17;
var duration= DEFAULT_DURATION_HOUR;
var granularity= PER_DAY;
var isFavorite=false;
var space=0;

function initialize() {
	var myLatlng = new google.maps.LatLng(37.870296,-122.258995);
	var mapOptions = {
		zoom: 16,
		center: myLatlng,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};

	$('#map-canvas').height(height*3/4);
	var map = new google.maps.Map(document.getElementById('map-canvas'),
			mapOptions);

	var kmlLayer = new google.maps.KmlLayer('https://dl.dropboxusercontent.com/u/12960227/UCBerkeleyParkingLotsGarages.kml',
	//var kmlLayer = new google.maps.KmlLayer('http://localhost:8080/UCBerkeleyParkingLotsGarages.kml',
	{
		suppressInfoWindows: true,
		preserveViewport: true
	});
	kmlLayer.setMap(map);

	google.maps.event.addListener(kmlLayer, 'click', function(kmlEvent) {
		var text = '<div class="well well-sm">'
                +'<span class="fav-garage">&#9733;&#9733; </span><span id="garage-name"><strong>'+kmlEvent.featureData.name+'</strong></span><span class="fav-garage"> &#9733;&#9733;</span><br>'
                +'<font color="#3366ff">Current Rate: </font>'
                +'<strong><span id="rate">Fetching</span></strong>'
                +'<hr>'

                +'<form class="form-horizontal">'
                +'<div class="form-group row" id="select-duration">'
                +'<label for="duration" class="col-lg-2 col-md-3 col-sx-6  control-label">Enter Duration (hour)</label>'
                +'<div class="col-lg-3 col-md-3 col-sx-6">'
                +'<input type="number" class="form-control" id="duration-value" value="2" min="1" max="24">'
                +'</div>'
                +'</div>'
                +'<div class="form-group row" id="select-space">'
                +'<label for="space" class="col-lg-2 col-md-3 col-sx-6 control-label">Enter Space (Optional)</label>'
                +'<div class="col-lg-3 col-md-3 col-sx-6">'
                +'<input type="number" class="form-control" id="space-value" value="0" min="0">'
                +'</div>'
                +'</div>'

                +'</div>'

				+'<div class="well well-sm">'
				+'<input id="park-btn" class="btn btn-primary" type="button" data-toggle="modal" data-target="#confirming" value="Park Here"/>&nbsp'
                +'<input onclick="changeGarage();" id="change-garage-btn" type="button" class="btn btn-warning" value="Change Garage"/>&nbsp'
                +'<input onclick="toggleFavorite();" id="mark-favorite-btn" type="button" class="btn" value="Mark as favorite"/>'
				+'</div>'

                + '<div class="well well-sm">'
				+ kmlEvent.featureData.description
				+ '</div>';
		showInContentWindow(text);
        $(".fav-garage").hide();
		$('html,body').scrollTop(0);
		$("#park-btn").attr("disabled","disabled");
		garageName = kmlEvent.featureData.name;
		fetchPrice();
	});

	function showInContentWindow(text) {
		var sidediv = document.getElementById('content-window');
		sidediv.innerHTML = text;
	}

	$('#confirming').on('show.bs.modal', function () {
		//Adjust Total Cost
        var current = window.localStorage["parkingGarage"];
        if (current){
            if (granularity == PER_DAY){
                var currentRate = window.localStorage["parkingRate"];
                if (rate > currentRate){
                    totalCost = rate - currentRate;
                }else{
                totalCost = 0;
                }
            }
        }

        $('#conf-garage').html(garageName);
		$('#conf-rate').html("$"+totalCost);

        //HOP
        $("#user-trans").val(window.localStorage['username']);
        $("#token-trans").val(window.localStorage['token']);
        $('#amount').val(""+totalCost);

		$('#confirmed').click({rate: rate, garageName: garageName, totalCost: totalCost, duration: duration, granularity: granularity, space: space},confirmed);
	});

    //why changeGarage function is undefined if put here while setTimePicker works

	google.maps.event.addListener(kmlLayer, 'metadata_changed', function () {
		$(".main").css("visibility","visible");
		$("#logo").hide();
	});
}

google.maps.event.addDomListener(window, 'load', initialize);
loadFavoriteAndTokenAndStatus();


