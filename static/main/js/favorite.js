var favorite = new Array();
function loadFavoriteAndToken(){
    $.get(SERVER_URL+"ugetfav/", {data:JSON.stringify({username: window.localStorage['username']})}, function(data, textStatus, jqXHR) {
        if (data){
            window.localStorage['token'] = data.token;
            $("#favorite-list").html("");
            for (var i=0; i<data.favorite.length; i++){
                favorite.push(data.favorite[i]);
            }
        }
        },"json")
        .done(function(){
            updateFavorite(favorite);
        })
        .fail(function(){

        });
}

function updateFavorite(garages){
    var text = " ";
    for (var i=0; i<garages.length; i++){
        var g = garages[i];
        text += '<input type="button" class="btn btn-warning" id="'
            +g
            +'" value="'
            +g
            +'" onclick="parkFav(this.id);"/>&nbsp';
    }
    if (garages.length == 0)
        $("#favorite-list").html("None");
    else
        $("#favorite-list").html(text);
}
function parkFav(g){
    garageName=g;
    $("#content-window").html(changeToParkFav(garageName));
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
        duration = this.value;
        totalCost = parseInt(duration,10)*r;
    });
}