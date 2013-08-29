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
var loading_css = $('#floatingBarsG');

function initialize() {
    loading_css.show();

	var myLatlng = new google.maps.LatLng(37.870296,-122.258995);
	var mapOptions = {
		zoom: 15,
		center: myLatlng,
		mapTypeId: google.maps.MapTypeId.ROADMAP
	};

    var map_canvas = $("#map-canvas");
    map_canvas.height(height*60/100);
	var map = new google.maps.Map(document.getElementById('map-canvas'),
			mapOptions);

	var kmlLayer = new google.maps.KmlLayer('https://dl.dropboxusercontent.com/u/63704802/UCBerkeleyParkingLotsGarages-noimg.kml',
	//var kmlLayer = new google.maps.KmlLayer('http://localhost:8080/UCBerkeleyParkingLotsGarages.kml',
	{
		suppressInfoWindows: true,
		preserveViewport: true
	});
	kmlLayer.setMap(map);

	google.maps.event.addListener(kmlLayer, 'click', function(kmlEvent) {
		var text = changeToParkingGarage(kmlEvent.featureData.name);
        text += '<div class="well well-sm">'
            + kmlEvent.featureData.description
			+ '</div>';

		showInContentWindow(text);
        $(".fav-garage").hide();
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
       loading_css.hide();

	});
}

google.maps.event.addDomListener(window, 'load', initialize);
loadFavoriteAndTokenAndStatus();


