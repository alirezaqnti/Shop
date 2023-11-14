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
	let loc = window.location;
	let path = loc.pathname.split('/');
	let res = await fetch(`/products/getsimilartopreview/${path[2]}`);
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
			x.forEach((element) => {
				let vars = JSON.parse(element.Varities);
				let var_ = vars[0];
				let sizes = var_.Size;
				let tag = ``;
				if (parseInt(sizes[0].OffPrice) > 0) {
					tag = `<a class="product-type two" href="#">ویژه</a>`;
					var price = `
			<div class='d-flex justify-content-evenly align-items-center'>
			<span>${getThousands(sizes[0].FinalPrice)} ریال</span>
			<small class='mr-1'>
			<del>
			${getThousands(element.Product_BasePrice)} ریال
			</del>
			</small>
			</div>
			`;
				} else {
					var price = `<span>${getThousands(
						sizes[0].FinalPrice
					)} ریال</span>
			`;
				}
				let sel = ``;
				for (let i = 0; i < sizes.length; i++) {
					const Si = sizes[i];
					let d;
					if (i == 0) {
						d = `
			  <div class="option selected" data-value="${var_.RPV}">
			  <span class="value" style="background-color: ${var_.Color};">
			  </span>
			  ${Si.Size}
			  </div>
			  `;
					} else {
						d = `
			  <div class="option" data-value="${var_.RPV}">
			  <span class="value" style="background-color: ${var_.Color};">
			  </span>
			  ${Si.Size}
			  </div>
			  `;
					}
					sel += d;
				}
				$('.MayLike')
					.owlCarousel()
					.trigger(
						'add.owl.carousel',
						`
				  
				  <div class="products-item">
					  <div class="top">
						${tag}
						  <a href="/products/${element.Slug}">
							<img src="/media/${element.Image_URL}" alt="${element.Name}" />
						  </a>
						  <div class="inner">
							  <h3>
							  <a href="/products/${element.Slug}">${element.Name}</a>
							  </h3>
							  ${price}
						  </div>
					  </div>
					  <div class="bottom">
						  <i class="bx bx-plus menuToggle"></i>
						  <div class="menu">
							  <ul>
								  <li class='menu-option' style="--i:0.1s;">
									<div class="select-menu">
									  <div class="select">
									  <span class="value" style="background-color: ${var_.Color};">
									  </span>
										<span class='varSize'>
										${sizes[0].Size}
										</span>
									  </div>
									  <div class="options-list">
										
										${sel}
										
									  </div>
									</div>
									 
								  </li>
								  <li  style="--i:0.2s;" class='AddToWish' data-target='${sizes[0].RPVS}'>
									<a href="#" >
									  <i class="bx bx-heart menu-option"></i>
									</a>
								  </li>
								  <li  style="--i:0.3s;" class='AddToCart' data-target='${sizes[0].RPVS}'>
									<a href="#">
									  <i class="bx bx-cart menu-option"></i>
									</a>
								  </li>
							  </ul>
						  </div>
					  </div>
				  </div>
			`
					)
					.trigger('refresh.owl.carousel');
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
