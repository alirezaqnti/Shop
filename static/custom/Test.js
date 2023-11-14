var username = '09128523035';
var password = 'Mohsenvafaei67';
var ptpTestMobile = '09177831766';
var authenticate = { security: { Username: username, Password: password } };
var url = 'http://94.182.154.28:1370/NiksmsWebservice.svc?wsdl';
var ptpModel = {
	security: {
		Username: username,
		Password: password,
	},
	model: {
		Message: [{ string: 'جهت تست نظیر به نظیر' }],
		SenderNumber: '9830006179',
		Numbers: [{ string: ptpTestMobile }],
		SendType: 'Normal',
		YourMessageId: [{ long: '1' }],
		//"SendOn": "2016-06-22T15:01:00.000Z" in parameter optional ast
	},
};
$.ajaxSetup({
	beforeSend: function (xhr, settings) {
		if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
			xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
		}
	},
});

$.ajax({
	type: 'POST',
	url: url,
	data: ptpModel,
	dataType: 'json',
	processData: false,
	contentType: 'text/xml; charset="utf-8"',
	success: function (response) {},
});
// soap.createClient(url, function (err, client) {
// 	//Ptp Sms
// });
