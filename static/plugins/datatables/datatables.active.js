(function ($) {
	'use strict';

	/*Default*/
	if ($('.data-table-default').length) {
		$('.data-table-default').DataTable({
			responsive: true,
			paging: false,
			language: {
				search: 'جستجو:',
			},
			columnDefs: [
				{
					targets: -1,
					className: 'dt-head-center',
				},
			],
		});
	}

	/*Default*/
	if ($('.data-table-nav-free').length) {
		$('.data-table-nav-free').DataTable({
			responsive: true,
		});
	}

	/*Export Buttons*/
	if ($('.data-table-export').length) {
		$('.data-table-export').DataTable({
			responsive: true,
			dom: 'Bfrtip',
			buttons: ['copy', 'csv', 'excel', 'pdf', 'print'],
			language: {
				paginate: {
					previous: '<i class="zmdi zmdi-chevron-left"></i>',
					next: '<i class="zmdi zmdi-chevron-right"></i>',
				},
			},
		});
	}
})(jQuery);
