/* user related */

/* Portfolio */
var get_dashboard_data_URL='api/data/dashboard';


/* Transactions */



/* Portfolio */
function get_dashboard_data(username, password, onSuccess){
	var data=new FormData();
	data.append('username', username);
	data.append('password', password);
	rawAjaxCall(get_dashboard_data_URL, "POST", true, data, onSuccess, onFailure);
}


// helpers ======================================================
/** generic ajax call */
/** other calls are just build onto this */
function rawAjaxCall(relativeURL,type,async_setting,data,onSuccess,onFailure){
	console.log("Firing request: " + relativeURL);
	$.ajax({
        url: relativeURL,
        contentType:false,
		processData: false,
		cache: false,
		async:async_setting,
        data:data,
        type: type, 
        success: onSuccess,
        error: onFailure,

    }); // end of the ajax call

}

/* common onFailure / onSuccess callback **/
var onFailure=function(jqHXR, textStatus, errorThrown){
	console.log('ajax error:' +textStatus + ' ' + errorThrown);
};