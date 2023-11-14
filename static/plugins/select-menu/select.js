$(document).on('click', '.select', function () {
	$(this).next('.options-list').toggleClass('active');
	$(this).toggleClass('active');
});
$(document).on('click', 'span.value', function () {
	$(this).next('.options-list').toggleClass('active');
	$(this).toggleClass('active');
});
$(document).on('click', '.option', function () {
	let parent = $(this).parent('.options-list');
	let opt = $(parent).children('.option.selected').first();
	$(opt).removeClass('selected');
	$(parent).prev('.select').html($(this).html());
	$(this).addClass('selected');
	$(parent).toggleClass('active');
	$(parent).prev('.select').toggleClass('active');
	let AC = $(this)
		.parents('.menu-option')
		.first()
		.closest('ul')
		.find('li.AddToCart');
	let AW = $(this)
		.parents('.menu-option')
		.first()
		.closest('ul')
		.find('li.AddToWish');
	let ACO = $(this)
		.parents('.menu-option')
		.first()
		.closest('ul')
		.find('li.AddToCompare');
	AC.attr('data-target', $(this).attr('data-value'));
	AW.attr('data-target', $(this).attr('data-value'));
	ACO.attr('data-target', $(this).attr('data-value'));
});
