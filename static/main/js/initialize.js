var app = {
	findLoggedInUser: function() {
		console.log("app.findLoggedInUser() called");
		this.store.findLoggedInUser(function (result) {
			console.log("findLoggedInUser result: " + result);
			if (result != null) {
				window.location.href= "/uprofile";
			} else {
				$(".main").css("visibility","visible");
				$("#spinning").hide();
			}
		});
	},

    initialize: function() {
        this.store = new WebSqlStore();
        this.findLoggedInUser();
    }
};

if (window.openDatabase){
	//app.initialize();
}else{
	//$(".main").css("visibility","visible");
	//$("#spinning").hide();
}

var storage = window.localStorage;
if ((storage.getItem("isLoggedIn") != null) && storage.getItem("username")) {
	window.location.href= "/uprofile";
} else {
	$(".main").css("visibility","visible");
	$("#spinning").hide();
}
var $alertBox = $("#alertBox");

$("#signIn").submit(function(e) {
    e.preventDefault();
	//window.location.href= "profile.html";
	handleLogin();
    return false;
});

function handleLogin() {
    var form = $("#signIn");    
    //disable the button so we can't resubmit while we wait
    $("#submitButton").attr("class", "btn-yellow disabled btn-block");
    var u = $("#inputUsername", form).val().trim();
    var p = $("#inputPassword", form).val().trim();
    console.log("click");
    if(u != '' && p != '') {
        $.get(SERVER_URL+"usignin/", {username:u,password:p}, function(data, textStatus, jqXHR) {
            if(data.user) {
                window.localStorage["username"] = u;
                window.localStorage["password"] = p;
                window.localStorage["token"] = data.token;
				window.localStorage["isLoggedIn"] = true;            
                window.location.href="/uprofile";
            } else {
                $alertBox.show();
                $alertBox.text("Please enter correct username and password");
            }
            $("#submitBtn").removeAttr("disabled");
        },"json").fail(function(){
                $alertBox.show();
                $alertBox.text("Server Error. Please try again.");
                $("#submitBtn").removeAttr("disabled");
            });
    } else {
        $alertBox.show();
        $alertBox.text("Please enter correct username and password");
        $('#submitButton').attr("class", "btn-yellow btn-block");



    }
}

