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

            <div class="col-sm-6">
            <div class="blog-item">
                <div class="top">
                    <a href="/blog/${post.Slug}">
                        <img src="${post.Poster}" alt="Blog" class="img-fluid" />
                    </a>
                    <span>${post.Created}</span>
                </div>
                <div class="bottom">
                    <h3>
                        <a href="/blog/${post.Slug}">
                            ${post.Title}
                        </a>
                    </h3>
                    <p class="text-truncate d-block">

                        ${post.Demo}
                    </p>
                    <a class="blog-btn" href="/blog/${post.Slug}">
                        ادامه مطلب
                        <i class="bx bx-plus"></i>
                    </a>
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
