$('#UIForm').ready(() => {
	$('input[name="passwordValid"]').on('keyup', function () {
		if (
			$('input[name="passwordValid"]').val() ==
			$('input[name="password"]').val()
		) {
			$('#message').html(' ').css('color', 'red');

			$('.UIReg').removeAttr('disabled');
		} else $('#message').html('مقادیر وارد شده یکسان نمی باشند').css('color', 'red');
	});
});
