$('.owl-carousel').owlCarousel({
	loop: true,
	margin: 10,
	rtl: true,
	nav: false,
	responsiveClass: true,
	responsive: {
		0: {
			items: 1,
		},
		600: {
			items: 3,
		},
		1000: {
			items: 5,

			loop: false,
		},
	},
});
cat = (id, level) => {
	data = {
		id: id,
	};
	var csrftoken = jQuery('[name=csrfmiddlewaretoken]').val();
	$.ajaxSetup({
		beforeSend: function (xhr, settings) {
			if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader('X-CSRFToken', getCookie('csrftoken'));
			}
		},
	});

	$.ajax({
		type: 'POST',
		url: ' /products/getcategories/ ',
		data: data,
		dataType: 'json',
		success: function (res, status) {
			$('#LOADER').addClass('d-none');
			$('#ul_' + id).empty();
			const response = res;
			if (level == 1) {
				if (response.length != 0) {
					for (let item = 0; item < response.length; item++) {
						const element = response[item];
						const slide = `<li>
                              <a  title="
                  ${element.CategoryName}
                  "
                              id='${element.id}'
                                href="javascript:void(0)"
                                onclick="insertParam('cat','${element.id}')">
                  ${element.CategoryName}
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
                                onclick="insertParam('cat','${id}')">
                                همه موارد این دسته
                                </a>
                            </li>`;
					$('#ul_' + id).prepend(slide);
				} else {
					const slide = `<li>
                              <a  title="همه موارد این دسته"
                                href="javascript:void(0)"
                                onclick="insertParam('cat','${id}')"
      
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
                              <a  title="${element.CategoryName}"
                              id='${element.id}'
                                href="javascript:void(0)"
                                onclick="insertParam('cat','${element.id}')">
                    ${element.CategoryName}
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
                                onclick="insertParam('cat','${id}')">
                                همه موارد این دسته
                                </a>
                            </li>`;
					$('#ul2_' + id).prepend(slide);
				} else {
					const slide = `<li>
                              <a  title="همه موارد این دسته"
                                href="javascript:void(0)"
                                onclick="insertParam('cat','${id}')">
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
                              <a  title="${element.CategoryName}"
                              id='${element.id}'
                                href="javascript:void(0)"
                                onclick="insertParam('cat','${element.id}')"
                                >
                                ${element.CategoryName}
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
                                onclick="insertParam('cat','${id}')"
                                >
                                همه موارد این دسته
                                </a>
                            </li>`;
					$('#ul3_' + id).append(slide);
				} else {
					const slide = `<li>
                              <a  title="همه موارد این دسته"
                                href="javascript:void(0)"
                                onclick="insertParam('cat','${id}')"
                                >همه موارد این دسته</a>
                            </li>`;
					$('#ul3_' + id).prepend(slide);
				}
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
				if (kvp[i].includes('cat=') || kvp[i].includes('txt=')) {
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
		if (x.next) {
			$('#MoreProd').attr('data-target', x.next);
			if ($('#MoreProd').hasClass('d-none')) {
				$('#MoreProd').removeClass('d-none');
			}
		} else {
			$('#MoreProd').addClass('d-none');
		}
		let result = x.results;
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
		}
		if (sort == 'minPrice') {
			result.sort(sortByminPrice);
		}
		if (sort == 'maxPrice') {
			result.sort(sortBymaxPrice);
		}
		let S = [];
		let RE = [];
		const V = x.results.map(({ Varities }) => JSON.parse(Varities));
		V.forEach((v) => {
			S.push(v.map(({ Size }) => Size));
		});
		S.forEach((s) => {
			s.forEach((element) => {
				RE.push(element.map(({ Size }) => Size));
			});
		});
		for (let i = 1; i < RE.length; i++) {
			const element = RE[i];
			let a = RE[0].concat(element);
			RE[0] = a;
		}
		const SizeFilter = [...new Set(RE[0])].sort();
		$('#Size').empty();
		SizeFilter.forEach((element) => {
			$('#Size').append(`
				<option value="${element}">${element}</option>
			`);
		});
		$('#Size').niceSelect('update');
		result.forEach((element) => {
			let vars = JSON.parse(element.Varities);
			let var_ = vars[0];
			let sizes = var_.Size;
			console.log(sizes);
			let tag = ``;
			if (parseInt(sizes[0].OffPrice) > 0) {
				tag = `<a class="product-type two" href="#">ویژه</a>`;
				var price = `
					<div class='d-flex justify-content-evenly align-items-center'>
					<span>${getThousands(sizes[0].FinalPrice)} ریال</span>
					<small class='mr-1'>
					<del>
					${getThousands(element.BasePrice)} ریال
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
					<div class="option selected" data-value="${Si.RPVS}">
					<span class="value" style="background-color: ${var_.Color};">
					</span>
					${Si.Size}
					</div>
					`;
				} else {
					d = `
						<div class="option" data-value="${Si.RPVS}">
						<span class="value" style="background-color: ${var_.Color};">
						</span>
						${Si.Size}
						</div>
						`;
				}
				sel += d;
			}
			$('.SearchResult').append(`

            <div div class="col-sm-6 col-lg-4 " >
              
            <div class="products-item">
            <div class="top">
              ${tag}
                <a href="/products/${element.Slug}">
                  <img src="/media/${element.Image_URL}" alt="${element.Name}" />
                </a>
                <div class="inner">
                    <h3>
                    <a href="/products/${element.slug}">${element.Name}</a>
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
                        <li  style="--i:0.4s;" class='AddToCompare' data-target='${sizes[0].RPVS}'>
                          <a href="#">
                            <i class="icon-compare"></i>
                          </a>
                        </li>
                    </ul>
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