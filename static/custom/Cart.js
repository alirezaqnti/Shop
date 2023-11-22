$('#City').change(function () {
	if ($(this).val() == 841) {
		$('.ShipWay').removeClass('d-none');
	} else {
		$('.ShipWay').addClass('d-none');
	}
});
$('input[name="ShippingWay"]').change(function () {
	let val = $('input[name="ShippingWay"]:checked').val();
	let total = parseInt($('.TotalPrice').attr('data-price'));

	if (val == 'post') {
		$('.ShippingPrice').html(getThousands('350000'));
		$('.TotalPrice').html(getThousands(String(total + 350000)));
	} else {
		$('.ShippingPrice').html(getThousands('150000'));
		$('.TotalPrice').html(getThousands(String(total + 150000)));
	}
});
$('#submitForm').click(function () {
	let Con = $('#Conditions').prop('checked');
	let Form = $('#CartForm');

	if (!Con) {
		let text = 'شرایط و قوانین استفاده را تایید نکرده اید';
		Failed(text);
		$('#Conditions').css('border-color', 'red');
	} else {
		Form.submit();
	}
});
$('#Coupon').on('input', function () {
	let val = $(this).val();
	$(this).val(val.toUpperCase());
	if (val != '') {
		$('.Coupon-Butt').removeClass('disabled');
		$('.Coupon-Butt').removeAttr('disabled');
	} else {
		$('.Coupon-Butt').addClass('disabled');
		$('.Coupon-Butt').attr('disabled', true);
	}
});
$('.Coupon-Butt').click(async function (e) {
	e.preventDefault();
	let Code = $('#Coupon').val();
	let RC = $(this).attr('data-RC');
	let res = await fetch('/warehouse/check-coupon/', {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ Code: Code, RC: RC }),
	});
	let info = await res.json();
	if (info.Check) {
		CartUpdate();
		$('#Coupon').attr('readonly', 'true');
		$('.Coupon-Butt').addClass('d-none');
		$('.Unattach-Butt').removeClass('d-none');
		Done(info.Mess);
	} else {
		Failed(info.Mess);
	}
});
$('.Unattach-Butt').click(async function (e) {
	e.preventDefault();
	let RC = $(this).attr('data-RC');
	let res = await fetch('/warehouse/unattach-coupon/', {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ RC: RC }),
	});
	let info = await res.json();
	if (info.Check) {
		CartUpdate();
		$('#Coupon').removeAttr('readonly');
		$('#Coupon').val('');
		$('.Coupon-Butt').removeClass('d-none');
		$('.Unattach-Butt').addClass('d-none');
		Done(info.Mess);
	} else {
		Failed(info.Mess);
	}
});

$(document).ready(function () {
	let total = parseInt($('.TotalPrice').attr('data-price'));
	let ShippingPrice = $('.ShippingPrice').attr('data-value');
	if (ShippingPrice == 'true') {
		$('.TotalPrice').html(getThousands(String(total + 350000)));
	}
});

$('.RemoveCart').click(async function (e) {
	e.preventDefault();
	let res = await fetch(`${loc.origin}/warehouse/removecart/`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
	});
	CartUpdate();
});

$(document).on('click', '.js-qty-button', async function (e) {
	LOADER();
	let input = $(this).parent().find('.qty-input');
	let v = input.val();
	let rcp = input.attr('data-rcp');
	console.log(rcp, v);
	let res = await fetch(`${loc.origin}/warehouse/change-cp/`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ RCP: rcp, Quantity: v }),
	});
	let info = await res.json();
	if (info.stat == 200) {
		LOADER();
		CartUpdate();
	} else {
		Failed(info.report);
	}
});
