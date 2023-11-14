$(document).ready(function () {
	let data = {};
	let checkData = {};
	// Initial data Starts
	// $('form').submit(function (e) {
	// 	e.preventDefault();
	// });
	$(document).keydown(function (e) {
		if (e.keyCode == 13) {
			let item = $('form');
			for (let i = 0; i < item.length; i++) {
				const element = item[i];
				if (!$(element).hasClass('d-none')) {
					let butt = $(element).find('button')[0];
					$(butt).trigger('click');
				}
			}
		}
	});
	$('.PHReg').on('click', function () {
		const phone_number = $('#PHRegForm .Phone').val();
		const sub = {
			Phone: phone_number,
		};
		let form = $('#PHRegForm');
		const url = '/users/register/phone/';
		if (CheckRequired(form)) {
			if (checkInitialData(phone_number)) {
				let res = AjaxReq(sub, url, dataChecked);
			}
		}
	});
	dataChecked = function () {
		$('#PHRegForm').fadeOut('slow', () => {
			const phone_number = $('#PHRegForm .Phone').val();
			$('#CodePhone').html(phone_number);
			$('#PHCodeForm').fadeIn('slow');
			$('#PHCodeForm').removeClass('d-none');
			$('#PHRegForm').css('display', 'none');
		});
	};
	checkInitialData = function (phone_number) {
		const phone_reg =
			/(0|\+98)?([ ]|-|[()]){0,2}9[0|1|2|3|4]([ ]|-|[()]){0,2}(?:[0-9]([ ]|-|[()]){0,2}){8}/gi;
		if (phone_number) {
			if (
				validate(phone_number, phone_reg) &&
				phone_number.length == 11
			) {
				checkData.phone_number = phone_number;
				return true;
			} else {
				checkData.phone_number = '';
				$('.toast-danger .toast-body').html(
					'شماره همراه خود را به درستی وارد نکرده اید'
				);
				$('.toast-danger').toast('show');
				return false;
			}
		} else {
			$('.toast-danger .toast-body').html(
				'شماره همراه خود را به درستی وارد نکرده اید'
			);
			$('.toast-danger').toast('show');
		}
		return false;
	};
	validate = (field, REG) => {
		return field.match(REG) ? true : false;
	};
	// Initial data Ends

	// Code Checking Starts
	$('.PHReg').on('click', function () {
		const phone_number = $('#PHRegForm .Phone').val();
		let form = $('#PHCodeForm');
		let Code = $('#PHCodeForm .Code').val();
		url = '/users/register/phone/code/';
		check = {
			Code: Code,
			Phone: phone_number,
		};
		if (CheckRequired(form)) {
			let res = AjaxReq(check, url, cellChecked);
		}
	});
	cellChecked = function () {
		data.Phone = checkData.phone_number;
		data.Email = checkData.email;
		data.Password = checkData.password;
		data.Phone_Confirm = true;
		$('#PHCodeForm').fadeOut('slow', () => {
			$('#UIForm').fadeIn('slow');
			$('#UIForm').removeClass('d-none');
			$('#PHCodeForm').css('display', 'none');
		});
	};
	$('.UIReg').on('click', function () {
		let form = $('#UIForm');

		const Name = $('input[name="Name"]').val();
		const Pass = $('input[name="password"]').val();
		const ValPass = $('input[name="passwordValid"]').val();
		const Con = $('#ConditionCheck').is(':checked');
		const Gen = $('.GenderCheck:checked').val();
		const phone_number = $('#PHRegForm .Phone').val();
		data.Name = Name;
		data.Phone = phone_number;
		data.Password = Pass;
		data.Gender = Gen;
		url = '/users/register/phone/code/submit/';
		if (CheckRequired(form)) {
			if (InfoCheck(Con, Pass, ValPass)) {
				const res = AjaxReq(data, url, dataSubmited);
			}
		}
	});
	InfoCheck = (Con, Pass, ValPass) => {
		$('.passexam').css('color', 'initial');
		$('.conexam').css('color', 'initial');
		if (Con) {
			if (checkPassword(Pass)) {
				if (Pass != ValPass) {
					$('#message')
						.html('مقادیر وارد شده یکسان نمی باشند')
						.css('color', 'red');
				} else return true;
			} else {
				$('.passexam').css('color', 'red');
			}
		} else $('.conexam').css('color', 'red');
	};
	dataSubmited = function () {
		let loc = window.location;
		$('.toast-success .toast-body').html(
			'ثبت نام شما با موفقیت انجام شد! وارد حساب کاربری خود شوید'
		);
		$('.toast-success').toast('show');
		setTimeout(() => (window.location.href = `${loc.origin}`), 3000);
	};
});
