$(function () {
	$('#wrapper').on('dragover', function (e) {
		e.preventDefault();
	});
	$('#img_preview').on('dragover', function (e) {
		e.preventDefault();
		$('#img_upload').addClass('on');
		$('#img_upload').removeClass('on');
	});
	$('#img_preview').on('drop', function (e) {
		dragoverHandler(e);
	});
	$('#img_upload').on('dragover', function (e) {
		e.preventDefault();
		$('#img_upload').addClass('on');
	});
	$('#img_upload').on('drop', function (e) {
		dragoverHandler(e);
		$('#img_upload').removeClass('on');
	});
});
function dragoverHandler(e) {
	e.preventDefault();
	e.stopPropagation();
	e.originalEvent.dataTransfer.getData('image/*');
	var files = e.originalEvent.dataTransfer.files;
	$('#img_upload input[type="file"]').prop('files', files);
}
function img_load(img) {
	if (img.files && img.files[0]) {
		let files = img.files;
		if (files.length > 5) {
			$(img).val('');
			Failed('5 تصویر حد مجاز آپلود می باشد');
		} else {
			RenderImages(files);
		}
	}
}

$(document).on('click', '.image-action', function () {
	let parent = $(this).parent().parent();
	let index = parseInt(parent.attr('data-No'));
	let input = $('#IMGInput')[0];
	const { files } = input;
	if (files) {
		const dt = new DataTransfer();
		for (let i = 0; i < files.length; i++) {
			const file = files[i];
			if (index !== i) {
				dt.items.add(file);
			}
		}
		input.files = dt.files;
		RenderImages(input.files);
	}
});

function RenderImages(files) {
	let SI = $('#img_preview .image-item.saved-image');
	if (SI.length > 0) {
		let item = $('#img_preview .image-item');
		for (let i = 0; i < item.length; i++) {
			const element = item[i];
			if (!$(element).hasClass('saved-image')) {
				$(element).remove();
			}
		}
		item = $('#img_preview .image-item');
		var j = item.length + 1;
	} else {
		$('#img_preview').empty();
		var j = 1;
	}
	for (let i = 0; i < files.length; i++) {
		const element = files[i];
		let reader = new FileReader();
		reader.onload = function (event) {
			// $('#img_upload').css('background-image','url('+event.target.result+')');
			$('#img_preview').append(`
				<div class="col-6 col-md-3 image-item" data-No='${i}'>
					<div class="img-wrapper">
						<img class='img-fluid' src='${event.target.result}' />
						<small>${j}</small>
						<a href="javascript:void(0)" class="image-action">
						<i class="fa fa-trash" aria-hidden="true"></i>
						</a>
					</div>
				</div>
				`);
			j++;
		};
		reader.readAsDataURL(element);
	}
}
