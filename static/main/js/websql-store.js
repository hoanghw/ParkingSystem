var WebSqlStore = function(successCallback, errorCallback) {

    this.initializeDatabase = function(successCallback, errorCallback) {
        var self = this;
        this.db = window.openDatabase("UsersDB", "1.0", "Users Info DB", 200000);
        this.db.transaction(
                function(tx) {
                    self.openTable(tx);
                },
                function(error) {
                    console.log("initializeDatabase Transaction error: " + error);
                    if (errorCallback) errorCallback();
                },
                function() {
                    console.log("initializeDatabase Transaction success");
                    if (successCallback) successCallback();
                }
        )
    }

    this.openTable = function(tx) {
        var sql = "CREATE TABLE IF NOT EXISTS users_info ( " +
            "id INTEGER PRIMARY KEY, " +
			"uid VARCHAR(50), " +
            "firstName VARCHAR(50), " +
            "lastName VARCHAR(50), " +
            "permit VARCHAR(50), " +
            "isParking BOOLEAN, " +
			"isLoggedIn BOOLEAN, " +
            "token VARCHAR(50), " +
            "username VARCHAR(50), " +
            "password VARCHAR(50), " +
            "email VARCHAR(50))";
        tx.executeSql(sql, null,
                function() {
                    console.log("openTable Create table success");
                },
                function(tx, error) {
                    alert("openTable Create table error: " + error.message);
                });
    }

    this.addUser = function(user, callback) {
        var sql = 
		tx.executeSql(sql, [user.id, user.uid, user.firstName, user.lastName, user.permit, user.isParking, user.isLoggedIn, user.token, user.username, user.password, user.email],
				function() {
					
				},
				function(tx, error) {
					
				});
        this.db.transaction(
            function(tx) {
                var sql = "INSERT OR REPLACE INTO users_info " +
            		"(id, uid, firstName, lastName, permit, isParking, isLoggedIn, token, username, password, email) " +
            		"VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

                tx.executeSql(sql, [user.id, user.uid, user.firstName, user.lastName, user.permit, user.isParking, user.isLoggedIn, user.token, user.username, user.password, user.email],
					function(tx, results) {
						console.log("addUser INSERT success");
                    	callback();
                });
            },
            function(error) {
              	alert("addUser INSERT error: " + error.message);
            }
        );
    }


    this.findByUserName = function(username, callback) {
        this.db.transaction(
            function(tx) {
                var sql = "SELECT u.uid, u.firstName, u.lastName, u.username, u.password, u.token, u.isParking, u.isLoggedIn u.permit, u.email " +
                    "FROM users_info u " +
                    "WHERE u.username=:username";

                tx.executeSql(sql, [username], function(tx, results) {
					console.log("findByUserName Transaction success");
                    callback(results.rows.length === 1 ? results.rows.item(0) : null);
                });
            },
            function(error) {
                alert("findByUserName Transaction Error: " + error.message);
            }
        );
    };
	
	this.findLoggedInUser = function(callback) {
		this.db.transaction(
            function(tx) {
                var sql = "SELECT * " +
                    "FROM users_info u " +
                    "WHERE u.isLoggedIn";

                tx.executeSql(sql, null , function(tx, results) {
					console.log("findLoggedInUser Transaction success");
                    callback(results.rows.length === 1 ? results.rows.item(0) : null);
                });
            },
            function(error) {
                alert("findLoggedInUser Transaction Error: " + error.message);
            }
        );
	};
	
	this.findCurrentParking = function(username,callback){
		this.db.transaction(
            function(tx) {

                var sql = "SELECT u.uid, u.firstName, u.lastName, u.username, u.password, u.token, u.isParking, u.isLoggedIn u.permit, u.email " +
                    "FROM users_info u " +
                    "WHERE u.username=:username && u.isParking";

                tx.executeSql(sql, [username], function(tx, results) {
					console.log("findCurrentParking Transaction success");
                    callback(results.rows.length === 1 ? results.rows.item(0) : null);
                });
            },
            function(error) {
                alert("findCurrentParking Transaction Error: " + error.message);
            }
        );
	};
	

    this.initializeDatabase(successCallback, errorCallback);

}
