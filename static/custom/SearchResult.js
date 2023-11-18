cat = async (id, level) => {
	let len = $(`#LI_${id} #ul${level}_${id} li`).length;
	if (!$(`#Cat_${id}`).hasClass('open') && len == 0) {
		data = {
			id: id,
		};
		let res = await fetch('/products/get-sub-categories/', {
			method: 'POST',
			headers: {
				Accept: 'application/json',
				'Content-Type': 'application/json',
			},
			body: JSON.stringify({ id: id }),
		});
		let info = await res.json();

		$(`#ul${level}_${id}`).empty();
		// const response = res;
		let cats = info.cats;
		cats.forEach((element) => {
			console.log(element);
			if (level == 1) {
				const slide = `
				<li>
					<a title="
						${element.name}
						"
						id='Cat_${element.id}'
						href="javascript:void(0)"
						onclick="insertParam('دسته بندی','${element.id}')">
						${element.name}
					</a>
					<div class="toggle-category js-toggle-category">
					<span>
						<i class="icon-angle-up" onclick="cat(${element.id},2)">
						</i>
					</span>
					</div>
					<ul class="category-list" style="display: none;" id='ul2_${element.id}'>

					</ul>
				</li>`;
				$(`#ul${level}_${id}`).append(slide);
			} else if (level == 2) {
				const slide = `<li>
						  <a  title="${element.name}"
							id='Cat_${element.id}'
								href="javascript:void(0)"
								onclick="insertParam('دسته بندی','${element.id}')">
								${element.name}
							</a>
						  <div class="toggle-category js-toggle-category">
							<span><i class="icon-angle-up" onclick="cat(${element.id},3)"></i></span>
						  </div>
						  <ul class="category-list" style="display: none;" id='ul3_${element.id}'>
	
						  </ul>
						</li>`;
				$(`#ul${level}_${id}`).append(slide);
			} else {
				const slide = `<li>
					<a title="${element.name}"
						id='Cat_${element.id}'
						href="javascript:void(0)"
						onclick="insertParam('دسته بندی','${element.id}')"
						>
						${element.name}
					</a>
						<div class="toggle-category js-toggle-category">
						<span><i class="icon-angle-up"></i></span>
						</div>
					</li>`;

				$(`#ul${level}_${id}`).append(slide);
			}
		});
		const slide = `<li>
			  <a  title="همه موارد این دسته"
				href="javascript:void(0)"
				onclick="insertParam('دسته بندی','${id}')"

				>همه موارد این دسته</a
			  >
			</li>`;
		$(`#ul${level}_${id}`).prepend(slide);
	}
};
function insertParam(key, value) {
	key = encodeURIComponent(key);
	value = encodeURIComponent(value);
	// kvp looks like ['key1=value1', 'key2=value2', ...]
	var kvp = document.location.search.substr(1).split('&');
	let i = 0;
	let params;
	if (key == 'cat') {
		params = `${key}=${value}&`;
	} else {
		for (; i < kvp.length; i++) {
			if (kvp[i].startsWith(key + '=')) {
				let pair = kvp[i].split('=');
				if (
					kvp[i].includes('دسته بندی=') ||
					kvp[i].includes('txt=') ||
					kvp[i].includes('sort=') ||
					kvp[i].includes('price=') ||
					kvp[i].includes('limit=')
				) {
					pair[1] = value;
					kvp[i] = pair.join('=');
				} else {
					if (pair[1] != value) {
						pair[1] += `,${value}`;
					}
					kvp[i] = pair.join('=');
				}
				break;
			}
		}
		if (i >= kvp.length) {
			kvp[kvp.length] = [key, value].join('=');
		}
		params = kvp.join('&');
	}
	document.location.search = params;
}
function removeKeyValue(parameter) {
	window.location = removeParams(parameter);
}
function removeParams(sParam) {
	var url = window.location.href.split('?')[0] + '?';
	var sPageURL = decodeURIComponent(window.location.search.substring(1)),
		sURLVariables = sPageURL.split('&'),
		sParameterName,
		i;

	for (i = 0; i < sURLVariables.length; i++) {
		sParameterName = sURLVariables[i].split('=');
		if (sParameterName[0] != sParam) {
			url = url + sParameterName[0] + '=' + sParameterName[1] + '&';
		}
	}

	return url.substring(0, url.length - 1);
}
$('.active-filter a').click(function () {
	const val = $(this).attr('data-type');
	if (val == 'cat') {
		loc.search = 'limit=15&';
	} else {
		removeKeyValue(val);
	}
});
$('.clear-filters').click(function () {
	window.location.search = '';
});
$('select[name="size"]').change(function () {
	let val = $(this).val();
	insertParam('size', val);
});
$('.priceSubmit').click(function () {
	let min = $('#minPrice').val();
	let max = $('#maxPrice').val();
	insertParam('price', [min, max]);
});
$('#SortCount').change(function () {
	let co = $(this).val();
	insertParam('limit', co);
});
$('#Sort').change(function () {
	let co = $(this).val();
	insertParam('sort', co);
});
let search;
if (loc.search == '') {
	search = 'limit=15';
} else {
	let s = loc.search;
	s = s.split('?');
	search = s[1];
}
if (!search.includes('limit')) {
	loc.search = `${search}&limit=15`;
}
var ResultsFetchURL = `/products/getsearchresult/?${search}`;
GetSearchResult = async function (URL) {
	let loc = window.location;
	let res = await fetch(URL);
	let info = await res.json();
	return info;
};
RenderSearchResult = function (URL) {
	let products = GetSearchResult(URL);

	products.then((x) => {
		console.log(x);
		$('.items-count span').html(x.count);
		if (x.next) {
			$('#MoreProd').attr('data-target', x.next);
			if ($('#MoreProd').hasClass('d-none')) {
				$('#MoreProd').removeClass('d-none');
			}
		} else {
			$('#MoreProd').addClass('d-none');
		}
		let result = x.results;
		for (let i = 0; i < result.length; i++) {
			const element = result[i];
			let F = element.Varities.Default.FinalPrice;
			element.FinalPrice = F;
		}
		const params = new Proxy(new URLSearchParams(window.location.search), {
			get: (searchParams, prop) => searchParams.get(prop),
		});
		let sort = params.sort;
		const sortByKeyA = (key) => (a, b) => b[key] - a[key];
		const sortByKeyD = (key) => (a, b) => a[key] - b[key];
		const sortByVisit = sortByKeyA('Visit');
		const sortByminPrice = sortByKeyD('FinalPrice');
		const sortBymaxPrice = sortByKeyA('FinalPrice');
		if (sort == 'view') {
			result.sort(sortByVisit);
			$('#Sort option[value="view"]').attr('selected', true);
		}
		if (sort == 'minPrice') {
			result.sort(sortByminPrice);
			$('#Sort option[value="minPrice"]').attr('selected', true);
		}
		if (sort == 'maxPrice') {
			result.sort(sortBymaxPrice);
			$('#Sort option[value="maxPrice"]').attr('selected', true);
		}
		result.forEach((PRD) => {
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
				<div class="price-new">${getThousands(Default.FinalPrice)} تومان
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
			$('.SearchResult').append(`
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
								<div class="prd-rating"><i class="icon-star-fill fill"></i><i
										class="icon-star-fill fill"></i><i
										class="icon-star-fill fill"></i><i
										class="icon-star-fill fill"></i><i
										class="icon-star-fill fill"></i>
								</div>
							</div>
							<div class="prd-rating justify-content-center">
								<i class="icon-star-fill fill"></i><i class="icon-star-fill fill"></i><i
									class="icon-star-fill fill"></i><i
									class="icon-star-fill fill"></i><i class="icon-star-fill fill"></i>
							</div>
							<h2 class="prd-title"><a href="/products/${PRD.Slug}">${PRD.Name}</a>
							</h2>
							<div class="prd-description">
								${PRD.Demo}
							</div>
							<div class="prd-action">
								<form action="#">
									<button class="btn js-prd-addtocart AddtoCart"
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
										<button class="btn js-prd-addtocart AddtoCart"
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
	});
};
RenderSearchResult(ResultsFetchURL);
$('#MoreProd').click(function () {
	let url = $(this).attr('data-target');
	RenderSearchResult(url);
});

GetTopSellPreview = async function () {
	let loc = window.location;
	let res = await fetch(`${loc.origin}/products/gettopsellpreview/`);
	let info = await res.json();
	return info;
};
RenderTopSellPreview = function () {
	let products = GetTopSellPreview();
	products.then((x) => {
		// $('.MayLike').empty();
		x.forEach((element) => {
			let vars = JSON.parse(element.Varities);
			let var_ = vars[0];
			let sizes = JSON.parse(var_.Size);
			let tag = ``;
			if (parseInt(sizes[0].fields.OffPrice) > 0) {
				tag = `<a class="product-type two" href="#">ویژه</a>`;
				var price = `
        <div class='d-flex justify-content-evenly align-items-center'>
        <span>${getThousands(sizes[0].fields.FinalPrice)} ریال</span>
        <small class='mr-1'>
        <del>
        ${getThousands(element.Product_BasePrice)} ریال
        </del>
        </small>
        </div>
        `;
			} else {
				var price = `<span>${getThousands(
					sizes[0].fields.FinalPrice
				)} ریال</span>
        `;
			}
			let sel = ``;
			for (let i = 0; i < sizes.length; i++) {
				const Si = sizes[i].fields;
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
                      <a href="/products/${element.slug}">
                        <img src="/media/${element.Image_URL}" alt="${element.Product_Name}" />
                      </a>
                      <div class="inner">
                          <h3>
                          <a href="/products/${element.slug}">${element.Product_Name}</a>
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
                                    ${sizes[0].fields.Size}
                                    </span>
                                  </div>
                                  <div class="options-list">
                                    
                                    ${sel}
                                    
                                  </div>
                                </div>
                                 
                              </li>
                              <li  style="--i:0.2s;" class='AddToWish' data-target='${sizes[0].fields.RPVS}'>
                                <a href="#" >
                                  <i class="bx bx-heart menu-option"></i>
                                </a>
                              </li>
                              <li  style="--i:0.3s;" class='AddToCart' data-target='${sizes[0].fields.RPVS}'>
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
	});
};
RenderTopSellPreview();

$('.SearchResult').on('click', '.AddToCompare', async function () {
	let RPVS = $(this).attr('data-target');
	console.log(RPVS);
	let res = await fetch('/products/add-to-compare/', {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
		body: JSON.stringify({ RPVS: RPVS }),
	});
	let info = await res.json();
	if (info.stat == 200) {
		$('.toast-success .toast-body').html(info.report);
		$('.toast-success').toast('show');
	} else if (info.stat == 201) {
		$('.toast-dark .toast-body').html(info.report);
		$('.toast-dark').toast('show');
	} else {
		$('.toast-danger .toast-body').html(info.report);
		$('.toast-danger').toast('show');
	}
});

$('.Compare').click(async function (e) {
	e.preventDefault();
	let res = await fetch('/products/compare-check/', {
		method: 'POST',
		headers: {
			Accept: 'application/json',
			'Content-Type': 'application/json',
		},
	});
	let info = await res.json();
	if (info.stat == 200) {
		window.location.href = '/products/compare/';
	} else if (info.stat == 201) {
		$('#CompareTipModal').modal('show');
	}
});
