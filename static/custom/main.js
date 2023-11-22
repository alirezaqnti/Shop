LOADER = function () {
	let load = $('.Loader');
	console.log(load, load.hasClass('d-none'));
	if (load.hasClass('d-none')) {
		$(document.body).css('overflow-y', 'hidden');
		load.removeClass('d-none');
	} else {
		$(document.body).css('overflow-y', 'auto');
		load.addClass('d-none');
	}
};
LOADER();

function Done(text) {
	$('.toast-success .toast-body').html(text);
	$('.toast-success').toast('show');
}
function Failed(text) {
	$('.toast-danger .toast-body').html(text);
	$('.toast-danger').toast('show');
}
function Warning(text) {
	$('.toast-dark .toast-body').html(text);
	$('.toast-dark').toast('show');
}
$('.num-input').on('input', function () {
	this.value = this.value.replace(/[^0-9.]/g, '').replace(/(\..*)\./g, '$1');
});
$('.noKey').on('keyDown', function () {
	$(this).val('');
});
$('.capital').on('input', function () {
	this.value = this.value.replace(/(\b)([a-zA-Z])/g, function (firstLetter) {
		return firstLetter.toUpperCase();
	});
});
$('.chPersian').on('input', function () {
	var p = /^[\u0600-\u06FF\s]+$/;
	if (!p.test($(this).val())) {
		$('#ModalResponse .modal-body p').html('کیبورد شما انگلیسی است');
		$('#ModalResponse').modal('show');
		setTimeout(() => {
			$('#ModalResponse').modal('hide');
		}, 3000);
		$(this).val('');
	}
});
$('.chEng').on('input', function () {
	var p = /^[A-Za-z][A-Za-z0-9]*$/;
	if (!p.test($(this).val())) {
		$('#ModalResponse .modal-body p').html('کیبورد شما فارسی است');
		$('#ModalResponse').modal('show');
		setTimeout(() => {
			$('#ModalResponse').modal('hide');
		}, 3000);
		$(this).val('');
	}
});
const getDeviceType = () => {
	const ua = navigator.userAgent;
	if (/(tablet|ipad|playbook|silk)|(android(?!.*mobi))/i.test(ua)) {
		return 'tablet';
	}
	if (
		/Mobile|iP(hone|od)|Android|BlackBerry|IEMobile|Kindle|Silk-Accelerated|(hpw|web)OS|Opera M(obi|ini)/.test(
			ua
		)
	) {
		return 'mobile';
	}
	return 'desktop';
};
getDeviceType();

getToken = () => {
	let loc = window.location;
	const res = fetch(`${loc.origin}/csrf/`, {
		credentials: 'include',
	})
		.then((res) => {
			var csrfToken = res['X-CSRFToken'];
			return csrfToken;
		})
		.catch(() => {
			return err;
		});
};

getToken();

AjaxReq = (data, url, func) => {
	var response = false;
	let csrf = $('input[name="csrfmiddlewaretoken"]').val();
	$.ajaxSetup({
		data: { csrfmiddlewaretoken: csrf },
		beforeSend: function (xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader('X-CSRFToken', csrf);
			}
		},
	});

	$.ajax({
		type: 'POST',
		url: url,
		data: data,

		dataType: 'json',
		success: async function (res, status) {
			console.log(res);
			if (res.stat == 200) {
				let empt = [];
				if (res.Docs) {
					func(res.Docs);
				} else {
					func(empt);
				}
			} else if (res.stat == 500) {
				Failed(res.report);
			} else if (res.stat == 202) {
				Failed((text = 'قبلا اضافه شده است'));
			} else if (res.stat == 203) {
				CartCheckRequired();
			} else if (res.stat == 300) {
				RedirectToRefferer();
			} else if (res.stat == 301) {
				PreLoginCall();
			} else if (res.stat == 302) {
				$('#EnterPhone').fadeOut('slow', () => {
					$('#LogIn').fadeIn('slow');
					$('#LogIn').removeClass('d-none');
				});
			} else if (res.stat == 303) {
				return res.data;
			} else if (res.stat == 304) {
				CartUpdate();
			} else if (res.stat == 305) {
				WishListUpdate();
			}
		},
		error: function (res, status) {
			$('#LOADER').addClass('d-none');
			$('#alertDanger strong').html('مشکلی پیش آمده !');
			$('#alertDanger span').html(' لطفا بعدا تلاش کنید');
			$('#alertDanger').removeClass('d-none');
			setTimeout(() => {
				$('#alertDanger').addClass('d-none');
			}, 5000);
		},
	});
};

RedirectToRefferer = async function () {
	let loc = window.location;
	let res = await fetch(`${loc.origin}/retriveurlsession/`);
	let info = await res.json();
	$('.toast-success .toast-body').html('با موفقیت وارد شدید');
	$('.toast-success').toast('show');
	setTimeout(
		() => (window.location.href = `${loc.protocol}//${info.URL}`),
		3000
	);
};

PreLoginCall = function () {
	let url = '/urlsession/';
	let data = {
		URL: window.location.href,
	};
	AjaxReq(data, url, PreLogin);
};

PreLogin = function () {
	$('.toast-dark .toast-body').html(
		'برای ادامه لازم است وارد حساب کاربری خود شوید'
	);
	$('.toast-dark').toast('show');
	setTimeout(() => (window.location.href = '/users/register/'), 3000);
};

PostLogin = async function (url) {
	$('.toast-dark .toast-body').html(
		'برای ادامه لازم است وارد حساب کاربری خود شوید'
	);
	$('.toast-dark').toast('show');
	setTimeout(() => (window.location.href = '/users/register/'), 3000);
};

function checkPassword(password) {
	var pattern = /^(?=.*\d)(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z]{8,}$/;
	if (pattern.test(password)) {
		return true;
	} else {
		return false;
	}
}

$('.categories-wrapper').mouseleave(function () {
	$('.categories-wrapper').fadeOut();
});

$(document).click(function (event) {
	if (
		!$(event.target).hasClass('menuToggle') &&
		!$(event.target).hasClass('nice-select') &&
		!$(event.target).hasClass('option') &&
		!$(event.target).hasClass('select-menu') &&
		!$(event.target).hasClass('select') &&
		!$(event.target).hasClass('value') &&
		!$(event.target).hasClass('varSize') &&
		!$(event.target).hasClass('options-list') &&
		!$(event.target).hasClass('menu-option')
	) {
		$('.menuToggle.active').removeClass('active');
	}
	if (!$(event.target).hasClass('SearchEngine')) {
		$('#SearchEngine').fadeOut();
	}
	if (
		!$(event.target).hasClass('categories-wrapper') &&
		!$(event.target).hasClass('nav-link') &&
		!$(event.target).hasClass('cat-pane') &&
		!$(event.target).hasClass('cat-list') &&
		!$(event.target).hasClass('cat-list-wrapper') &&
		!$(event.target).hasClass('ad-item') &&
		!$(event.target).hasClass('container-fluid') &&
		!$(event.target).hasClass('cat-item')
	) {
		$('.categories-wrapper').fadeOut();
	}
});

$('#State').change(async function () {
	$('.ShipWay').addClass('d-none');
	const val = $(this).val();
	let res = await fetch('/getcity/', {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ id: val }),
	});
	let info = await res.json();
	$('#City').empty();
	for (let index = 0; index < info.data.length; index++) {
		const element = info.data[index];
		$('#City').append(
			`<option value='` +
				element['id'] +
				`'>` +
				element['title'] +
				`</option>`
		);
	}
	$('#City').niceSelect('update');
});
$(document).ready(function () {
	LOADER();
});
