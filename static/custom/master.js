var loc = window.location;

$('body').on('click', '.Removefromcart', function (e) {
	e.preventDefault();
	let slug = $(this).attr('data-RCP');
	let data = {
		RCP: slug,
	};
	let url = `/warehouse/removefromcart/`;
	let res = AjaxReq(data, url, CartUpdate);
});

$('.WishlistTable').on('click', 'button', function (e) {
	e.preventDefault();
	let slug = $(this).attr('data-target');
	let tr = $(this).parents('tr')[0];
	let data = {
		RW: slug,
	};
	let url = `/warehouse/removefromwishlist/`;
	let res = AjaxReq(data, url);
	if (res) {
		$(tr).fadeOut(1000);
		$('.WishlistTable').remove(tr);
		WishListUpdate();
	}
});
$(document).on('click', '.AddToWish', function (e) {
	e.preventDefault();
	let RPVS = $(this).attr('data-product');
	let data = {
		RPVS: RPVS,
	};
	let url = `${loc.origin}/warehouse/addtowishlist/`;
	AjaxReq(data, url, AddToWishlistCallBack);
});

AddToWish = function (RPVS, e) {
	e.preventDefault();
	let data = {
		RPVS: RPVS,
	};
	let url = `${loc.origin}/warehouse/addtowishlist/`;
	AjaxReq(data, url, AddToWishlistCallBack);
};

AddToWishlistCallBack = async function () {
	let text = 'محصول به لیست علاقه مندی ها اضافه شد';
	$('.toast-success .toast-body').html(text);
	$('.toast-success').toast('show');

	WishListUpdate();
};

WishListUpdate = async function () {
	let res = await fetch(`${loc.origin}/warehouse/getwishlist/`);
	let info = await res.json();

	$('.WishlistHead').html(`${info.count} محصول`);
	$('.WishlistBadge').html(`${info.count}`);
	let Pros = info.Pros;
	$('.WishlistTable').empty();
	for (let i = 0; i < Pros.length; i++) {
		const element = Pros[i];
		var si = ``;
		var color = ``;
		if (element.Size) {
			si = ` سایز ${element.Size}`;
		}
		if (element.Color) {
			color = `<span class='value' style='background-color:${element.Color}'></span>`;
		}

		$('.WishlistTable').append(`
		<tr>
		<th scope="row">
		  <img src="/media/${element.Pic}" alt="Cart" />
		</th>
		<td>
		  <span class="rate">${element.Name}
			<span class="value" style="background-color: ${element.Color};"></span>
			سایز ${element.Size}
		  </span>
		</td>
		<td>
		  <a class="btn btn-outline-dark" href="#">
			<i class="fa fa-cart-plus" aria-hidden="true"></i>
		  </a>
		</td>
		<td>
		  <button type='button' class="close btn btn-link" data-target="${element.RW}">
			<i class="bx bx-x"></i>
		  </button>
		</td>
	  </tr>
            `);
	}
};
$(document).on('click', '.AddToCart', function (e) {
	e.preventDefault();
	let RPVS = $(this).attr('data-product');
	let Quantity = $('#QuantityINP').val();
	Quantity = Quantity != undefined ? Quantity : 1;
	let data = {
		RPVS: RPVS,
		Quantity: Quantity,
	};
	let url = `${loc.origin}/warehouse/addtocart/`;
	AjaxReq(data, url, AddedToCart);
});

AddToCart = function (RPV, e) {
	let data = {
		RPVS: RPV,
	};
	let url = `${loc.origin}/warehouse/addtocart/`;
	AjaxReq(data, url, AddedToCart);
};

AddedToCart = function () {
	let text = 'محصول به سبد خرید شما اضافه شد';
	$('.toast-success .toast-body').html(text);
	$('.toast-success').toast('show');
	if ($('.Cart-Footer').hasClass('d-none')) {
		$('.Cart-Footer').removeClass('d-none');
	}

	CartUpdate();
};
CartUpdate = async function () {
	let res = await fetch(`${loc.origin}/warehouse/getcart/`, {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
	});
	let info = await res.json();
	console.log(info);
	$('#dropdnMinicart .Cart-TotalPrice').html(
		`${getThousands(info.TotalPrice)} ریال`
	);
	$('#CartModal .CartModalTotalDiscount').html(
		`${getThousands(info.TotalDiscount)} ریال`
	);
	$('#CartModal .CartModalShippingPrice').html(
		`${getThousands(info.ShippingPrice)} ریال`
	);
	$('.Header-Count').html(`${info.count}`);
	$('.Header-TotalPrice').html(`${getThousands(info.TotalPrice)}`);
	$('.Cart-TotalPrice').html(`${getThousands(info.TotalPrice)}`);
	let crds = $('#ModalCartProducts .minicart-prd');
	for (let i = 0; i < crds.length; i++) {
		const element = crds[i];

		element.remove();
	}
	$('#CartTable').empty();
	$('#CartTable').append(`
		<div class="cart-table-prd cart-table-prd--head py-1 d-none d-md-flex">
		<div class="cart-table-prd-image text-center">
			تصویر
		</div>
		<div class="cart-table-prd-content-wrap">
			<div class="cart-table-prd-info">نام</div>
			<div class="cart-table-prd-qty">تعداد</div>
			<div class="cart-table-prd-price">قیمت</div>
			<div class="cart-table-prd-action">&nbsp;</div>
		</div>
	</div>
		`);
	let Pros = info.Pros;
	if (Pros.length == 0) {
		$('.minicart-empty').removeClass('d-none');
		$('.minicart-drop-total').addClass('d-none');
		$('.minicart-drop-total').css('opacity', '0');
	} else {
		$('.minicart-empty').addClass('d-none');
		$('.minicart-drop-fixed').removeClass('d-none');
		$('.minicart-drop-total').removeClass('d-none');
		$('.minicart-drop-total').css('opacity', '1');
	}

	for (let i = 0; i < Pros.length; i++) {
		const element = Pros[i];

		var si = ``;
		var price = ``;
		var color = ``;
		if (element.Size && element.Size != 0) {
			si = `- سایز ${element.Size}`;
		}
		if (element.Color) {
			color = `<span class='value' style='background-color:${element.Color}'></span>`;
		}
		if (element.discount > 0) {
			price = `
			<div class="price-old"><span class="pr CP-Offless">${getThousands(
				element.Offless
			)} </span> ریال</div>
			<div class="price-new"><span class="pr CP-Fee">${getThousands(
				element.Fee
			)}</span> ریال</div>
			`;
		} else {
			price = `
			<div class="price-new"><span class="pr CP-Fee">${getThousands(
				element.Fee
			)}</span> ریال</div>
			`;
		}
		$('#ModalCartProducts').append(`
		<div class="minicart-prd row">
			<div class="minicart-prd-image image-hover-scale-circle col">
				<a href="/products/${element.RPVS}">
				<img class="lazyload fade-up"
						src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
						data-src="/media/${element.Pic}" alt=""></a>
			</div>
			<div class="minicart-prd-info col">
				<div class="minicart-prd-tag">${element.ColorName} ${si}</div>
				<h2 class="minicart-prd-name"><a href="/products/${element.RPVS}">${element.Name}</a></h2>
				<div class="minicart-prd-qty"><span class="minicart-prd-qty-label">تعداد : </span><span
						class="minicart-prd-qty-value">${element.Quantity}</span></div>
				<div class="minicart-prd-price prd-price">
				${price}
				</div>
			</div>
			<div class="minicart-prd-action">
				<a href="javascript:void(0)" data-RCP="${element.RCP}"
					class="js-product-remove Removefromcart" data-line-number="1"><i
						class="icon-recycle"></i></a>
			</div>
		</div>
	`);

		$('#CartTable').append(`
		<div class="cart-table-prd">
			<div class="cart-table-prd-image">
				<a href="/products/${
					element.RPVS
				}" class="prd-img"><img class="lazyload fade-up"
						src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
						data-src="/media/${element.Pic}" alt=""></a>
			</div>
			<div class="cart-table-prd-content-wrap">
				<div class="cart-table-prd-info">
					<div class="cart-table-prd-price">
					${price}
					</div>
					<h2 class="cart-table-prd-name">
					<a href="/products/${element.RPVS}">${element.Name}</a>
					</h2>
				</div>
				<div class="cart-table-prd-qty">
					<div class="qty qty-changer">
						<button class="decrease"></button>
						<input type="text" class="qty-input" value="${element.Quantity}" data-min="1"
							data-max="${element.Max}">
						<button class="increase"></button>
					</div>
				</div>
				<div class="cart-table-prd-price-total">
					<span class="pr CP-Amount">${getThousands(element.Amount)}</span> ریال
				</div>
			</div>
			<div class="cart-table-prd-action">
				<a href="javascript:void(0)" data-RCP="${element.RCP}"
					class="cart-table-prd-remove Removefromcart" data-tooltip="حذف محصول"><i
						class="icon-recycle"></i></a>
			</div>
		</div>
		`);
	}
};
$('#catMenu-tabContent').on('click', '.nav-link', function () {
	let target = $(this).attr('data-target');
	$(`#${target}`).tab('show');
});
$('#catLI').mouseenter(async () => {
	if ($('.categories-wrapper').css('display') == 'none') {
		if ($('#catMenu').children().length == 0) {
			const info = await fetch('/products/getcategories/');
			const res = await info.json();
			$('#catMenu').empty();
			$('#catMenu-tabContent').empty();
			for (let i = 0; i < res.length; i++) {
				let active = '';
				let show = '';
				if (i == 0) {
					show = 'show';
					active = ' active';
				}
				const element = res[i];
				const item = `
				<button class="nav-link ${show}" id="catMenu-${i}-tab" data-toggle="tab" data-target="#catMenu-${i}"
				  type="button" role="tab" aria-controls="catMenu-${i}" aria-selected="false">${element.Name}</button>
							`;
				$('#catMenu').append(item);
				var items = '';
				for (let j = 0; j < element.children.length; j++) {
					const child = element.children[j];
					items += `<li class="title cat-item">
				  <a href="/products/results/?cat=${child.parent.id}">
				  ${child.parent.Name}
				  </a>
				</li>`;
					if (child.children.length != 0) {
						for (let k = 0; k < child.children.length; k++) {
							const grand = child.children[k];
							const item = `
							<li class='cat-item'>
							  <a href="/products/results/?cat=${grand.id}">${grand.Name}</a>
							</li>
						`;
							items += item;
						}
					}
				}

				let pane = ` <div class="tab-pane cat-pane ${
					show + active
				} fade" id="catMenu-${i}" role="tabpanel"
				  aria-labelledby="catMenu-${i}-tab">
				  <div class="cat-list-wrapper">
					<ul class="cat-list">
					   
					  ${items}
					</ul>
				  </div>
	  
				</div>`;
				$('#catMenu-tabContent').append(pane);
			}
		}
		// $('#catMenu').children().first().addClass('active show');
		// $('#catMenu-tabContent').children().first().addClass('active show');
		$('.categories-wrapper').fadeIn();
	} else {
		$('.categories-wrapper').fadeOut();
	}
});
$('#catLI').click(function () {
	$('#catLI').trigger('mouseenter');
});
cat = (id, level) => {
	let data = {
		id: id,
	};
	let csrftoken = jQuery('[name=csrfmiddlewaretoken]').val();
	$.ajaxSetup({
		beforeSend: function (xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader('X-CSRFToken', csrftoken);
			}
		},
	});

	$.ajax({
		type: 'POST',
		url: ' /get-sub-cat/ ',
		data: {
			getdata: JSON.stringify(data),
		},
		dataType: 'json',
		success: function (res, status) {
			$('#LOADER').addClass('d-none');
			if (res.stat == 200) {
				$('#ul_' + id).empty();
				const response = res.cats;
				if (level == 1) {
					if (response.length != 0) {
						for (let item = 0; item < response.length; item++) {
							const element = response[item];
							const slide = `<li>
							  <a  title="
				  ${element.name}
				  "
							  id='
				  ${element.id}
				  '
								href="javascript:void(0)"
								onclick="insertParam('cat','
				  ${element.slug}
				  ')">
				  ${element.name}
				  </a>
							  <div class="toggle-category js-toggle-category">
								<span><i class="icon-angle-up" onclick="cat(${element.id},2)"></i></span>
							  </div>
							  <ul class="category-list" style="display: none;" id='ul2_${element.id}'>
								
							  </ul>
							</li>`;
							$('#ul_' + id).append(slide);
						}
						const slide = `<li>
							  <a  title="همه موارد این دسته"
								href="javascript:void(0)"
								onclick="insertParam('cat','${slug}')">
								همه موارد این دسته
								</a>
							</li>`;
						$('#ul_' + id).append(slide);
					} else {
						const slide = `<li>
							  <a  title="همه موارد این دسته"
								href="javascript:void(0)"
								onclick="insertParam('cat','${slug}')"
	  
								>همه موارد این دسته</a
							  >
							</li>`;
						$('#ul_' + id).append(slide);
					}
				} else if (level == 2) {
					if (response.length != 0) {
						for (let item = 0; item < response.length; item++) {
							const element = response[item];
							const slide = `<li>
							  <a  title="${element.name}"
							  id='${element.id}'
								href="javascript:void(0)"
								onclick="insertParam('cat','${element.slug}')">
					${element.name}
				  </a>
							  <div class="toggle-category js-toggle-category">
								<span><i class="icon-angle-up" onclick="cat(${element.id},3)"></i></span>
							  </div>
							  <ul class="category-list" style="display: none;" id='ul3_${element.id}'>
								
							  </ul>
							</li>`;
							$('#ul2_' + id).append(slide);
						}
						const slide = `<li>
							  <a  title="همه موارد این دسته"
								href="javascript:void(0)"
								onclick="insertParam('cat','${slug}')">
								همه موارد این دسته
								</a>
							</li>`;
						$('#ul2_' + id).append(slide);
					} else {
						const slide = `<li>
							  <a  title="همه موارد این دسته"
								href="javascript:void(0)"
								onclick="insertParam('cat','${slug}')">
								همه موارد این دسته
								</a>
							</li>`;
						$('#ul2_' + id).append(slide);
					}
				} else {
					if (response.length != 0) {
						for (let item = 0; item < response.length; item++) {
							const element = response[item];
							const slide = `<li>
							  <a  title="${element.name}"
							  id='${element.id}'
								href="javascript:void(0)"
								onclick="insertParam('cat','${element.slug}')"
								>
								${element.name}
				  </a>
							  <div class="toggle-category js-toggle-category">
								<span><i class="icon-angle-up"></i></span>
							  </div>
							</li>`;
							$('#ul3_' + id).append(slide);
						}
						const slide = `<li>
							  <a  title="همه موارد این دسته"
								href="javascript:void(0)"
								onclick="insertParam('cat','${slug}')"
								>
								همه موارد این دسته
								</a>
							</li>`;
						$('#ul3_' + id).append(slide);
					} else {
						const slide = `<li>
							  <a  title="همه موارد این دسته"
								href="javascript:void(0)"
								onclick="insertParam('cat','${slug}')"
								>همه موارد این دسته</a>
							</li>`;
						$('#ul3_' + id).append(slide);
					}
				}
			}
			if (res.stat == 500) {
				$('#alertSuccess').removeClass('d-none');
				setTimeout(() => {
					$('#alertSuccess').addClass('d-none');
				}, 5000);
			}
		},
		error: function (res, status) {
			$('#LOADER').addClass('d-none');
			$('#alertError').html('مشکلی پیش آمده است لطفا مجددا تلاش کنید');
			$('#alertError').removeClass('d-none');
			setTimeout(() => {
				$('#alertError').addClass('d-none');
			}, 5000);
		},
	});
};
$('#searchBox').click(function () {
	let val = $(this).val();
	if (val != '') {
		$('#searchBox').trigger('keyup');
	}
});
$('#searchBox').on('keyup', async function () {
	let val = $(this).val();
	let res = await fetch('/products/getsearchengine/', {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ Txt: val }),
	});
	let info = await res.json();
	$('#SearchEngine ul').empty();
	if (info.length != 0) {
		info.forEach((element) => {
			$('#SearchEngine ul').append(`
			<li>
			${element.Name}
			</li>
			`);
		});
	}
	$('#SearchEngine ul').append(`
		<li>
		<a href='/products/results/?txt=${val}&'>
		<b>
		<i class="fas fa-font"></i>
		جستجو:
		</b>
		<span>${val}</span>
		</a>
		</li>
		`);
	$('#SearchEngine').fadeIn();
});

$(function () {
	var init = 0;
	$('#searchBox').keyup(function (event) {
		if (event.keyCode == 13) {
			let val = $('#searchBox').val();
			window.location.href = `/products/results/?txt=${val}`;
		}
	});
	$('.SearchEngineBtn').click(function () {
		if (init == 0) {
			$('#wiki').animate({
				width: '300px',
			});
			setTimeout(() => {
				$('#searchBox').css('display', 'inline-block');
			}, 500);
			$('#NavBarScearchBox').fadeIn();

			init = 1;
		} else {
			$('#NavBarScearchBox').fadeOut();
			$('#searchBox').css({
				display: 'none',
			});
			$('#wiki').animate({
				width: '60px',
			});
			$('#SearchEngine').fadeOut();
			$('#searchBox').val('');

			init = 0;
		}
	});
});

$('.products-area').on('click', '.menuToggle', function () {
	$('.menuToggle.active').not(this).removeClass('active');
	$(this).toggleClass('active');
});

function CheckRequired(form) {
	var $form = $(form);

	if (
		$form.find('input[required]').filter(function () {
			return this.value === '';
		}).length > 0
	) {
		$('.toast-danger .toast-body').html(
			'اطلاعات خواسته شده را کامل وارد کنید'
		);
		$('.toast-danger').toast('show');
		return false;
	} else return true;
}

$('#LoginCode').on('click', function () {
	const phone_number = $('#InitialForm #phone_number').val();
	const LoginCode = true;
	const sub = {
		Phone: phone_number,
		LoginCode: LoginCode,
	};
	const url = '/users/register/phone/';
	let res = AjaxReq(sub, url, LoginFunc);
});

$('.LoginCode').on('click', function () {
	$('.PHPass').fadeOut('slow', () => {
		$('.PHPass').addClass(`d-none`);
		$('.PHCode').fadeIn('slow');
		$('.PHCode').removeClass('d-none');
		$('.PHPass').css('display', 'none');
	});
});
$('.LoginPass').on('click', function () {
	$('.PHCode').fadeOut('slow', () => {
		$('.PHCode').addClass(`d-none`);
		$('.PHPass').fadeIn('slow');
		$('.PHPass').removeClass('d-none');
		$('.PHCode').css('display', 'none');
	});
});
$('.LoginPassCode').on('click', function () {
	$('.PHCodeValid').fadeOut('slow', () => {
		$('.PHCodeValid').addClass(`d-none`);
		$('.PHPass').fadeIn('slow');
		$('.PHPass').removeClass('d-none');
		$('.PHCodeValid').css('display', 'none');
	});
});
$('.FastLoginPass').click(() => {
	let form = $('.PHPass');
	let data = {};
	const Pass = $('.PHPass input[name="passWord"]').val();
	const phone_number = $('.PHPass .Phone').val();
	data.Phone = phone_number;
	data.Password = Pass;
	data.Type = 'Pass';
	url = '/users/login/';
	if (CheckRequired(form)) {
		const res = AjaxReq(data, url, userLoggedIN);
	}
});
$('.FastLoginPhone').click(() => {
	let form = $('.PHPass');
	let data = {};
	const phone_number = $('.PHCode .Phone').val();
	data.Phone = phone_number;
	data.Type = 'Phone';
	url = '/users/login/';
	if (CheckRequired(form)) {
		const res = AjaxReq(data, url, CodeCallback);
	}
});
$('.FastLoginResend').click(() => {
	let form = $('.PHPass');
	let data = {};
	const phone_number = $('.PHCode .Phone').val();
	data.Phone = phone_number;
	data.Type = 'Phone';
	url = '/users/login/';
	if (CheckRequired(form)) {
		const res = AjaxReq(data, url, CodeCallback);
	}
});

CodeCallback = function () {
	const phone_number = $('.PHCode .Phone').val();
	start_on();

	$('#CodePhone').html(phone_number);
	$('.PHCode').fadeOut('slow', () => {
		$('.PHCode').addClass(`d-none`);
		$('.PHCodeValid').fadeIn('slow');
		$('.PHCodeValid').removeClass('d-none');
		$('.PHCode').css('display', 'none');
	});
};

$('.FastLoginCode').click(() => {
	let form = $('.PHCodeValid');
	let data = {};
	const Code = $('.PHCodeValid .Code').val();
	const phone_number = $('.PHCode .Phone').val();
	data.Phone = phone_number;
	data.Code = Code;
	data.Type = 'Code';
	url = '/users/login/';
	if (CheckRequired(form)) {
		const res = AjaxReq(data, url, userLoggedIN);
	}
});
userLoggedIN = function () {
	$('.toast-success .toast-body').html('با موفقیت وارد شدید');
	$('.toast-success').toast('show');
	setTimeout(() => (window.location.href = loc.origin), 3000);
};
var timerid = 0;
var count = 120;
var timer = document.getElementById('timer');
var timm = document.getElementById('timm');
function start_down() {
	count--;
	if (count <= 0) {
		clearInterval(timerid);
	}
	if (count > 0) {
		var min = Math.floor(count / 60);
		var sec = count % 60;
		timer.innerHTML = ('0' + min).slice(-2) + ':' + ('0' + sec).slice(-2);
	} else {
		$('#time').addClass('d-none');
		$('.FastLoginResend').removeClass('d-none');
	}
}
function start_on() {
	start_down();
	timerid = setInterval(start_down, 1000);
}
