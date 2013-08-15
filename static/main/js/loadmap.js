// JavaScript Document
var width = $(window).width();
var height = $(window).height();
var garageName="default";
var rate=17;
var totalCost=17;
var duration= DEFAULT_DURATION_HOUR;
var granularity= PER_DAY;

function initialize() {
	var myLatlng = new google.maps.LatLng(37.870296,-122.258995);
	var mapOptions = {
		zoom: 15,
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
		var text = '<div class="well well-sm" id="garage-info">'
				+ '<span id="garage-name"><strong>'+kmlEvent.featureData.name+'</strong></span>'
				+ '</div>'

				+ '<div class="well well-sm">'
				+ kmlEvent.featureData.description
				+ '</div>'

				+'<div class="well well-sm">'
				+'<font color="#3366ff">Current Rate: </font>'
				+'<span id="rate">Fetching</span>'
				+'<br/>'

				+'<div id="select-duration" style="display:none;">'

				+'<font color="#3366ff">Pick Duration: </font>'

                +'<div id="slider-div">'
                +'<input type="text" id="slider" value="" data-slider-min="1" data-slider-max="24" data-slider-step="1" data-slider-value="2" data-slider-orientation="horizontal" data-slider-selection="after"data-slider-tooltip="hide">'
                +'</div>'

                +'<div class="row">'
                +'<div class="col-3"><input type="number" class="form-control" id="slider-value" value="2"></div><span class="help-block">hour(s)</span>'
                +'</div>'

                +'</div>'
				+'</div>'

				+'<div class="well well-sm">'
				+'<input id="park-btn" class="btn btn-primary" type="button" data-toggle="modal" data-target="#confirming" value="Park Here"/>'
				+'</div>'
				+'<br/>' ;
		showInContentWindow(text);
		$('html,body').scrollTop(0);
		$("#park-btn").attr("disabled","disabled");
		garageName = kmlEvent.featureData.name;
		fetchPrice();
	});

	function showInContentWindow(text) {
		var sidediv = document.getElementById('content-window');
		sidediv.innerHTML = text;
	}
	function fetchPrice(){
		var tempStorage = window.sessionStorage;
		if (false){
            //console.log('in tempStorage');
			rate=tempStorage[garageName+"_rate"];
			totalCost=tempStorage[garageName+"_totalCost"];
		}else{
			$.get(SERVER_URL+"getrate/", {data:JSON.stringify({garage:garageName, username: window.localStorage['username']})}, function(data, textStatus, jqXHR) {
				var jsonObj = data;
				if (jsonObj){
					switch (jsonObj.granularity){
						case PER_HOUR:
							console.log('per hour');
							$("#select-duration").show();
                            $("#slider").width(width*60/100);
                            rate = jsonObj.magnitude;
                            granularity = PER_HOUR;
                            duration = DEFAULT_DURATION_HOUR;
		                    totalCost = duration*rate;
                            $("#rate").text("$"+rate+"/hour");
							setTimePicker(rate);
							break
						case PER_DAY:
							console.log('per day');
							rate = jsonObj.magnitude;
							totalCost = jsonObj.magnitude;
                            granularity = PER_DAY;
                            duration = 1;
                            $("#rate").text("$"+rate+"/day");
							break;
						default:
							console.log('default');
                            rate = jsonObj.magnitude;
							totalCost = jsonObj.magnitude;
                            granularity = PER_DAY;
                            duration = 1;
                            $("#rate").text("$"+rate+"/day");

					}
					tempStorage[garageName+"_rate"] = rate;
					tempStorage[garageName+"_totalCost"] = totalCost;
					tempStorage[garageName]="was fetched at...";

                    //Quick hack
                    window.localStorage['token']=jsonObj.token;
				}
				else {
					console.log('cannot parse');
            		rate = 10;
					totalCost = 10;
                    granularity = PER_DAY;
                    duration = 1;
                    $("#rate").text("$"+rate+"/day");
            	}
        	},"json").always(function(){
		        $("#park-btn").removeAttr("disabled");
                });
		}
	}

	$('#confirming').on('show.bs.modal', function () {
		$('#conf-garage').html(garageName);
		$('#conf-rate').html("$"+totalCost);

        //HOP
        $("#user-trans").val(window.localStorage['username']);
        $("#token-trans").val(window.localStorage['token']);
        $('#amount').val(""+totalCost);
		$('#confirmed').click({rate: rate, garageName: garageName, totalCost: totalCost, duration: duration, granularity: granularity},confirmed);
	});

	google.maps.event.addListener(kmlLayer, 'metadata_changed', function () {
		$(".main").css("visibility","visible");
		$("#logo").hide();
	});
}

function setTimePicker(r){
	$('#slider').slider().on('slide', function(ev){
        $('#slider-value').val(ev.value);
        duration = ev.value;
        totalCost = parseInt(duration,10)*r;
    });
    $('#slider-value').on('keyup change', function(){
        $('#slider').slider('setValue', this.value);
        duration = this.value;
        totalCost = parseInt(duration,10)*r;
    });
}
google.maps.event.addDomListener(window, 'load', initialize);

