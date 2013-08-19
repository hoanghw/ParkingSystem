function signOut(){
	window.localStorage.removeItem("isLoggedIn");
    window.localStorage.removeItem("username");
    window.localStorage.removeItem("password");
    window.localStorage.removeItem("token");
    window.localStorage.removeItem('parkingGarage');
    window.localStorage.removeItem('parkingEndTime');
    window.localStorage.removeItem('parkingRate');
	window.location.href= "ulogin";
}

