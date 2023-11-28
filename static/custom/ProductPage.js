$(document).ready(function () {
	var max_fields = 5; //Maximum allowed input fields
	var STRwrapper = $('.STRwrapper'); //Input fields wrapper
	var Weakwrapper = $('.Weakwrapper'); //Input fields wrapper
	var AddSTR = $('#AddSTR'); //Add button class or ID
	var AddWeak = $('#AddWeak'); //Add button class or ID
	var x = 1; //Initial input field is set to 1
	var y = 1; //Initial input field is set to 1

	//- Using an anonymous function:

	//When user click on add input button
	$(AddSTR).click(function (e) {
		e.preventDefault();
		//Check maximum allowed input fields
		if (x < max_fields) {
			x++; //input field increment
			//add input field
			$(STRwrapper).append(`
                        <div class="form-group">
                            <input type="text" class="form-control" name="STR" />
                            <a href = "javascript:void(0);" class= "remove_field" >
                                <i class="fas fa-times"></i>
                            </a>
                        </div>
                            `);
		}
	});
	$(AddWeak).click(function (e) {
		e.preventDefault();
		//Check maximum allowed input fields
		if (y < max_fields) {
			y++; //input field increment
			//add input field
			$(Weakwrapper).append(`
                        <div class="form-group">
                            <input type="text" class="form-control" name="Weak" />
                            <a href = "javascript:void(0);" class= "remove_field" >
                                <i class="fas fa-times"></i>
                            </a>
                        </div>
                    `);
		}
	});

	//when user click on remove button
	$(STRwrapper).on('click', '.remove_field', function (e) {
		e.preventDefault();
		$(this).parent().remove(); //remove inout field
		x--; //inout field decrement
	});
	//when user click on remove button
	$(Weakwrapper).on('click', '.remove_field', function (e) {
		e.preventDefault();
		$(this).parent().remove(); //remove inout field
		x--; //inout field decrement
	});
});

$('.color-item').click(async function () {
	let RPV = $(this).attr('data-value');
	let obj = await fetch(`/products/getvariety/${RPV}`);
	let x = await obj.json();
	console.log(x);
	let Sizes = x.Size;
	$('.SubsWrapper').addClass('d-none');
	$('.prd-block_price-old-wrap').addClass('d-none');

	if (Sizes.length > 1) {
		$('#SingleOptionSelector-1').empty();
		$('ul[data-select-id="SingleOptionSelector-1"]').empty();
		for (let i = 0; i < Sizes.length; i++) {
			const element = Sizes[i];
			if (i == 0) {
				$('#SingleOptionSelector-1').append(`
						<option value="${element.RPVS}" selected="selected"
						data-finalprice="${element.FinalPrice}"
						data-offprice="${element.OffPrice}"
						data-baseprice="${x.BasePrice}"
						data-discount="${element.Discount}"
						data-quantity="${element.Quantity}"
						>
							${element.Size}
						</option>
				`);
				$('ul[data-select-id="SingleOptionSelector-1"]').append(`
					<li class="active"
					data-finalprice="${element.FinalPrice}"
						data-offprice="${element.OffPrice}"
						data-baseprice="${x.BasePrice}"
						data-discount="${element.Discount}"
						data-quantity="${element.Quantity}">
						<a href="#" data-value="${element.RPVS}">
							<span class="value">${element.Size}</span>
						</a>
					</li>
				`);
			} else {
				$('#SingleOptionSelector-1').append(`
						<option value="${element.RPVS}"
						data-finalprice="${element.FinalPrice}"
						data-offprice="${element.OffPrice}"
						data-baseprice="${x.BasePrice}"
						data-discount="${element.Discount}"
						data-quantity="${element.Quantity}">
							${element.Size}
						</option>
				`);
				$('ul[data-select-id="SingleOptionSelector-1"]').append(`
					<li
					data-finalprice="${element.FinalPrice}"
						data-offprice="${element.OffPrice}"
						data-baseprice="${x.BasePrice}"
						data-discount="${element.Discount}"
						data-quantity="${element.Quantity}">
						<a href="#" data-value="${element.RPVS}">
							<span class="value">${element.Size}</span>
						</a>
					</li>
				`);
			}
		}
		$('.SubsWrapper').removeClass('d-none');
	}
	$('.FinalPrice').html(`${getThousands(x.Size[0].FinalPrice)}`);
	if (x.Size[0].Quantity < 6) {
		$('.QuantityProgress').attr('data-left-in-stock', x.Size[0].Quantity);
		$('.QuST').html(x.Size[0].Quantity);
		$('.QuantityProgress').removeClass('d-none');
	} else {
		$('.QuantityProgress').addClass('d-none');
	}
	if (x.Size[0].OffPrice > 0) {
		$('.BasePrice').html(`${getThousands(x.BasePrice)}`);
		$('.OffPrice').html(`${getThousands(x.Size[0].OffPrice)}`);
		$('.DiscountPerc').html(`(${getThousands(x.Size[0].Discount)} %)`);
		$('.prd-block_price-old-wrap').removeClass('d-none');
	} else {
		$('.prd-block_price-old-wrap').addClass('d-none');
	}
	$('.RPVS').html(x.Size[0].RPVS);
	if (x.Size[0].Quantity > 0) {
		$('.Existence').html('موجود');
	} else {
		$('.Existence').html('ناموجود');
	}
	$('.AddToWish').attr('data-product', x.Size[0].RPVS);
	$('.AddToCart').attr('data-product', x.Size[0].RPVS);
	$('.Notify-btn').attr('data-slug', x.Size[0].RPVS);
	$('#SizeSelect').val(x.Size[0].RPVS);
	$('#QuantityINP').attr('data-max', x.Size[0].Quantity);
	$('#QuantityINP').val(1);
});

$('#SingleOptionSelector-1').change(function () {
	let FinalPrice = $(
		'ul[data-select-id="SingleOptionSelector-1"] li.active'
	).attr('data-finalprice');
	let OffPrice = $(
		'ul[data-select-id="SingleOptionSelector-1"] li.active'
	).attr('data-offprice');
	let BasePrice = $(
		'ul[data-select-id="SingleOptionSelector-1"] li.active'
	).attr('data-baseprice');
	let RPVS = $(this).val();
	let Quantity = $(
		'ul[data-select-id="SingleOptionSelector-1"] li.active'
	).attr('data-quantity');
	let Discount = $(
		'ul[data-select-id="SingleOptionSelector-1"] li.active'
	).attr('data-discount');
	$('.FinalPrice').html(`${getThousands(FinalPrice)}`);
	if (Quantity < 6) {
		$('.QuantityProgress').attr('data-left-in-stock', Quantity);
		$('.QuST').html(Quantity);
		$('.QuantityProgress').removeClass('d-none');
	} else {
		$('.QuantityProgress').addClass('d-none');
	}
	if (OffPrice > 0) {
		$('.BasePrice').html(`${getThousands(BasePrice)}`);
		$('.OffPrice').html(`${getThousands(OffPrice)}`);
		$('.DiscountPerc').html(`(${getThousands(Discount)} %)`);
		$('.prd-block_price-old-wrap').removeClass('d-none');
	} else {
		$('.prd-block_price-old-wrap').addClass('d-none');
	}
	$('.AddToWish').attr('data-target', RPVS);
	$('.AddToCart').attr('data-target', RPVS);
	$('.Notify-btn').attr('data-slug', RPVS);
	$('.RPVS').html(RPVS);
	if (Quantity > 0) {
		$('.Existence').html('موجود');
	} else {
		$('.Existence').html('ناموجود');
	}
});

GetSimilarToPreview = async function () {
	let slug = $('.prd-block_title').attr('data-slug');
	let res = await fetch(`/products/getsimilartopreview/${slug}`);
	let info = await res.json();
	return info;
};

RenderSimilarToPreview = function () {
	let products = GetSimilarToPreview();
	$('.MayLike').empty();
	products.then((x) => {
		if (x.length == 0) {
			let p = $('.MayLike').parents('.products-area');
			p.addClass('d-none');
		} else {
			x.forEach((PRD) => {
				let vars = PRD.Varities;
				let Images = PRD.Images;
				let Default = vars.Default;
				let Lables = vars.Lables;
				let Vars = vars.Vars;
				let Price = '';
				if (Default.Discount > 0) {
					Price = `
					<div class="price-old">${getThousands(PRD.BasePrice)} ریال
					</div>
					<div class="price-new">${getThousands(Default.FinalPrice)} ریال
					</div>
					`;
				} else {
					Price = `
					<div class="price-new">${getThousands(Default.FinalPrice)} ریال
					</div>
					`;
				}
				let Label = '';
				let OS = '';
				for (let i = 0; i < Lables.length; i++) {
					const element = Lables[i];
					if (element.Label == 'label-new') {
						Label += `<div class="label-new"><span>جدید</span></div>`;
					} else if (element.Label == 'label-sale') {
						Label = `
						<div class="label-sale"><span>${element.Value}%- <span class="sale-text">فروش
									ویژه</span></span>
							<div class="countdown-circle">
								<div class="countdown js-countdown" data-countdown="2021/07/01">
								</div>
							</div>
						</div>
						`;
					} else if (element.Label == 'prd-outstock') {
						OS = 'prd-outstock';
					}
				}
				let Colors = '';
				for (let i = 0; i < Vars.length; i++) {
					const element = Vars[i];
					Colors += `
						<li>
							<a class="#" data-toggle="tooltip" data-placement="right" title="${element.ColorName}" style='background-color:${element.ColorCode}'>
							</a>
						</li>
						`;
				}
				let Imgs = '';
				for (let i = 0; i < Images.length; i++) {
					const element = Images[i];
					if (i == 0) {
						Imgs += `
						<li data-image="/media/${element.Image}" class="active">
							<a href="#" class="js-color-toggle" data-toggle="tooltip" data-placement="left">
								<img
									src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
									data-src="/media/${element.Image}"
									class="lazyload fade-up" alt="Color Name">
							</a>
						</li>
						`;
					} else {
						Imgs += `
						<li data-image="/media/${element.Image}" >
							<a href="#" class="js-color-toggle" data-toggle="tooltip" data-placement="left">
								<img
									src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
									data-src="/media/${element.Image}"
									class="lazyload fade-up" alt="Color Name">
							</a>
						</li>
						`;
					}
				}
				let Stars = '';
				for (let i = 0; i < PRD.Rate; i++) {
					Stars += '<i class="icon-star-fill fill"></i>';
				}
				$('.MayLike').append(`
					<div class="prd prd--style2 prd-labels--max prd-labels-shadow ${OS}">
					<div class="prd-inside">
						<div class="prd-img-area">
							<a href="/products/${PRD.Slug}" class="prd-img image-hover-scale image-container"
								style="padding-bottom: 128.48%">
								<img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
									data-src="/media/${Images[0].Image}"
									alt="${PRD.Name}" class="js-prd-img lazyload fade-up">
								<div class="foxic-loader"></div>
								<div class="prd-big-squared-labels">
									${Label}
								</div>
							</a>
							<div class="prd-circle-labels">
								<a 
									href="#" 
									class="circle-label-qview js-prd-quickview prd-hide-mobile"
									data-src="ajax/ajax-quickview.html">
									<i class="icon-eye"></i>
									<span>مشاهده سریع</span>
								</a>
								<div
									class="colorswatch-label colorswatch-label--variants js-prd-colorswatch">
									<i class="icon-palette"><span class="path1"></span><span
											class="path2"></span><span class="path3"></span><span
											class="path4"></span><span class="path5"></span><span
											class="path6"></span><span class="path7"></span><span
											class="path8"></span><span class="path9"></span><span
											class="path10"></span></i>
									<ul>
										${Colors}
									</ul>
								</div>
							</div>
							<ul class="list-options color-swatch">
								${Imgs}
							</ul>
						</div>
						<div class="prd-info">
							<div class="prd-info-wrap">
								<div class="prd-info-top">
									<div class="prd-rating">
										${Stars}
									</div>
								</div>
								<div class="prd-rating justify-content-center">
								${Stars}
								</div>
								<h2 class="prd-title"><a href="/products/${PRD.Slug}">${PRD.Name}</a>
								</h2>
								<div class="prd-description">
									${PRD.Demo}
								</div>
								<div class="prd-action">
									<form action="#">
										<button class="btn js-prd-addtocart AddToCart"
											data-product='${Default.RPVS}'>افزودن
											به سبد خرید</button>
									</form>
								</div>
							</div>
							<div class="prd-hovers">
								<div class="prd-circle-labels">
									
									<div class="prd-hide-mobile"><a href="#"
											class="circle-label-qview js-prd-quickview"
											data-src="ajax/ajax-quickview.html"><i
												class="icon-eye"></i><span>مشاهده
												سریع</span></a></div>
								</div>
								<div class="prd-price">
									${Price}
								</div>
								<div class="prd-action">
									<div class="prd-action-left">
										<form action="#">
											<button class="btn js-prd-addtocart AddToCart"
												data-product='${Default.RPVS}'>افزودن
												به سبد خرید</button>
										</form>
									</div>
								</div>
							</div>
						</div>
					</div>
				</div>
				`);
			});
		}
	});
};
RenderSimilarToPreview();

$('.Notify-btn').click(async function (e) {
	e.preventDefault();
	let RPVS = $(this).attr('data-slug');
	let res = await fetch('/products/notify/', {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ RPVS: RPVS }),
	});
	let info = await res.json();
	console.log(info);
	if (info.stat == 200) {
		$('.toast-success .toast-body').html(info.report);
		$('.toast-success').toast('show');
	} else {
		$('.toast-danger .toast-body').html(info.report);
		$('.toast-danger').toast('show');
	}
});
