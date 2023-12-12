let search;
if (loc.search == '') {
	search = 'limit=15';
} else {
	let s = loc.search;
	s = s.split('?');
	search = s[1];
}
if (!search.includes('limit')) {
	loc.search = `limit=15&${search}`;
}
var ResultsFetchURL = `/blog/posts/getposts/?${search}`;
GetPosts = async function (URL) {
	let res = await fetch(URL);
	let info = await res.json();
	return info;
};
RenderPosts = function (URL) {
	let Posts = GetPosts(URL);
	Posts.then((x) => {
		if (x.next) {
			$('#MorePost').attr('data-target', x.next);
			if ($('#MorePost').hasClass('d-none')) {
				$('#MorePost').removeClass('d-none');
			}
		} else {
			$('#MorePost').addClass('d-none');
		}
		let result = x.results;
		for (let i = 0; i < result.length; i++) {
			const post = result[i];
			$('.Post-Wrapper').append(`
			<div class="post-prw">
				<div class="row vert-margin-middle">
					<div class="post-prw-img col-md-7">
						<a href="/blog/post/${post.RPO}">
							<img src="data:image/gif;base64,R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
								data-src="${post.Poster}" class="lazyload fade-up" alt="">
						</a>
					</div>
					<div class="post-prw-text col-md-11">
						<div class="post-prw-links">
							<div class="post-prw-date"><i class="icon-calendar"></i>${post.Created}</div>
							<div class="post-prw-date"><i class="icon-star"></i>${post.Rate}/5</div>
						</div>
						<h4 class="post-prw-title"><a href="/blog/post/${post.RPO}">${post.Title}</a>
						</h4>
						<div class="post-prw-teaser">${post.Demo}</div>
						<div class="post-prw-btn">
							<a href="/blog/post/${post.RPO}" class="btn btn--sm">مطالعه بیشتر</a>
						</div>
					</div>
				</div>
			</div>
            `);
		}
	});
};
RenderPosts(ResultsFetchURL);
$('#MorePost').click(function () {
	let url = $(this).attr('data-target');
	RenderPosts(url);
});
