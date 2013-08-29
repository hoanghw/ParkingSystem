var favorite = new Array();
function loadFavoriteAndTokenAndStatus(){
    $.get(SERVER_URL+"ugetfav/", {data:JSON.stringify({username: window.localStorage['username']})}, function(data, textStatus, jqXHR) {
        if (data){
            if (data.error){
                signOut();
            }else{
                window.localStorage['token'] = data.token;
                $("#favorite-list").html("");
                for (var i=0; i<data.favorite.length; i++){
                    favorite.push(data.favorite[i]);
                }
                if (Object.keys(data.isParking).length != 0){
                    window.localStorage['parkingGarage'] = data.isParking.garage;
                    window.localStorage['parkingEndTime'] = data.isParking.endTime;
                    window.localStorage['parkingRate'] = data.isParking.rate;
                    $('#content-window').html(changeToParked(data.isParking.garage,data.isParking.endTime));
                }else{
                    window.localStorage.removeItem('parkingGarage');
                    window.localStorage.removeItem('parkingEndTime');
                    window.localStorage.removeItem('parkingRate');
                    $('#content-window').html(changeToNotParked());
                }
            }
        }
        },"json")
        .done(function(){
            updateFavorite(favorite);
        })
        .fail(function(){
            signOut();
        });
}

function updateFavorite(garages){
    var l = garages.length;
    if (l == 0){
        $("#favorite-list").html("No favorite garages selected");
    }else if (l == 1){
        var text = '<input type="button" style="margin-bottom: 0px; padding-bottom: 0px;" class="btn btn-xs btn-danger" id="'
                +garages[0]
                +'" value="'
                +garages[0]
                +'" onclick="parkFav(this.id);"/>';
        $("#favorite-list").html(text);
    }else{
        var text ='<div class="btn-group"><button type="button" class="btn btn-xs btn-info dropdown-toggle" data-toggle="dropdown">Click here ... <span class="caret"></span></button>'
            +'<ul style="text-align: center; background-color: whitesmoke;" class="dropdown-menu" role="menu">';
        for (var i=0; i<l; i++){
            text +='<li><input type="button" class="btn btn-xs btn-danger" style="margin-bottom: 5px;" id="'
                +garages[i]
                +'" onclick="parkFav(this.id);" value="'
                +garages[i]
                +'"></li>';
        }
        text += '</ul></div>'
        $("#favorite-list").html(text);
    }
}
function parkFav(g){
    garageName=g;
    $("#content-window").html(changeToParkingGarage(garageName));
    fetchPrice();
}
function fetchPrice(){
		var tempStorage = window.sessionStorage;
		if (false){
            //console.log('in tempStorage');
			//rate=tempStorage[garageName+"_rate"];
			//totalCost=tempStorage[garageName+"_totalCost"];
		}else{
			$.get(SERVER_URL+"getrate/", {data:JSON.stringify({garage:garageName, username: window.localStorage['username']})}, function(data, textStatus, jqXHR) {
				var jsonObj = data;
				if (jsonObj){
					switch (jsonObj.granularity){
						case PER_HOUR:
							console.log('per hour');
							$("#select-duration").show();
                            $("#select-space").show();
                            $("#slider").width(width*60/100);
                            rate = jsonObj.magnitude;
                            granularity = PER_HOUR;
                            duration = DEFAULT_DURATION_HOUR;
		                    totalCost = duration*rate;
                            $("#rate").text("$"+rate+"/hour");
							setTimePicker(rate);
                            setSpacePicker();
							break
						case PER_DAY:
							console.log('per day');
                            $("#select-duration").hide();
                            $("#select-space").show();
							rate = jsonObj.magnitude;
							totalCost = jsonObj.magnitude;
                            granularity = PER_DAY;
                            duration = 1;
                            $("#rate").text("$"+rate+"/day");
                            setSpacePicker();
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

                    if (jsonObj.isFavorite){
                        markFavorite(false);
                    }else{
                        unmarkFavorite(false);
                    }
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

function setTimePicker(r){
    $('#duration-value').on('keyup change', function(){
        duration = Math.abs(parseInt(this.value,10));
        if (isNaN(duration)&&(duration==0)){
            duration = DEFAULT_DURATION_HOUR;
        }
        totalCost = duration*r;
    });
}
function setSpacePicker(){
    $('#space-value').on('keyup change', function(){
        space = parseInt(this.value,10);
    });
}