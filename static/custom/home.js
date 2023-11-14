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
GetProductToPreview = async function () {
	let loc = window.location;
	let res = await fetch(`${loc.origin}/products/getproductstopreview/`);
	let info = await res.json();
	return info;
};
RenderProductsToPreview = function () {
	let products = GetProductToPreview();
	products.then((x) => {
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
			$('.ProductToPreview')
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
RenderProductsToPreview();

GetTopSellPreview = async function () {
	let loc = window.location;
	let res = await fetch(`${loc.origin}/products/gettopsellpreview/`);
	let info = await res.json();
	return info;
};
RenderTopSellPreview = function () {
	let products = GetTopSellPreview();
	products.then((x) => {
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
			$('.TopsellPreview')
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

$('.slider').slick({
	dots: true,
	infinite: false,
	speed: 300,
	slidesToShow: 1,
	slidesToScroll: 1,
	responsive: [
		{
			breakpoint: 1024,
			settings: {
				slidesToShow: 1,
				slidesToScroll: 1,
				infinite: true,
				dots: true,
			},
		},
		{
			breakpoint: 600,
			settings: {
				slidesToShow: 1,
				slidesToScroll: 1,
			},
		},
		{
			breakpoint: 480,
			settings: {
				slidesToShow: 1,
				slidesToScroll: 1,
			},
		},
		// You can unslick at a given breakpoint now by adding:
		// settings: "unslick"
		// instead of a settings object
	],
});
