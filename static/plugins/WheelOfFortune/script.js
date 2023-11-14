$(document).ready(async function () {
	async function GetPermission() {
		let res = await fetch('/warehouse/fortune/getpermission/');
		let info = await res.json();
		return info.stat;
	}
	let permission = GetPermission();
	permission.then(async (x) => {
		console.log('permission:', x);
		if (x == 200) {
			let res = await fetch('/getwheeldata/');
			let info = await res.json();
			let Prizes = info[0].Prizes;
			var number = Prizes.length;
			var angleToFit = Math.ceil(360 / number) * 0.57;
			var width = 2 * 250 * Math.sin((angleToFit * Math.PI) / 360);
			var Angles = [];
			var sectionAngle = angleToFit * 0.33 + angleToFit;
			var currRot = sectionAngle;
			var wheel = $('.wheel');

			var round = 360 / number;
			let cl = ['#93291E', '#5c1912'];
			for (x = 0; x < number; x++) {
				let bc = x % 2 == 0 ? cl[0] : cl[1];
				const prize = Prizes[x];
				rotate = Math.ceil(round) * x;
				Angles.push(rotate);
				wheel.append(`
			<div class="section" 
			id="sec-${rotate}" 
			data-value="${prize.RFP}" 
			data-target="${rotate}"
			data-Type="${prize.Null}"
			style="transform:rotate(${rotate}deg);
			border-color:${bc} transparent;
			border-width:255px ${width}px 0;
			transform-origin:${parseInt(width - 1)}px 254px;">
		  <p><b> ${prize.Title}</b></p>
		  </div>
		  `);
			}
			$('.button-wrap').click(function () {
				if ($(this).attr('disabled') == 'disabled') {
					Failed(
						'امکان استفاده ی مجدد تا فعال شدن گردونه شانس بعدی غیرفعال است'
					);
				} else {
					$(this).attr('disabled', true);
					var count = 0;
					var rng = Math.floor(Math.random() * 30 + 50);
					setTimeout(function () {
						$('.button-wrap').addClass('tick');
					}, 425);

					var interval = setInterval(function () {
						currRot = currRot + sectionAngle / 2;
						wheel.css('transform', 'rotate(' + currRot + 'deg)');
						count++;
						if (count == rng) {
							clearInterval(interval);
							setTimeout(function () {
								$('.button-wrap').removeClass('tick');
							}, 150);
							setTimeout(function () {
								let goal = getRotationDegrees(wheel);
								let target = 378 - goal;
								let closest = 0;
								for (let i = 1; i <= Angles.length; i++) {
									const prev = Angles[i - 1];
									const curr = Angles[i];
									if (target >= prev && target < curr) {
										closest = prev;
									} else if (target == curr) {
										closest = curr;
									}
								}
								let prize = $(
									`.section[data-target=${closest}]`
								);
								let RFP = prize.attr('data-value');
								let type = prize.attr('data-type');
								let text = $(
									`.section[data-target=${closest}] p b`
								).html();
								ShowModal(text, type, RFP);
							}, 500);
						}
					}, 100);
				}
			});
			async function ShowModal(Text, Type, RFP) {
				Type = Type == 'false' ? false : true;
				var message;
				if (!Type) {
					$('#FortuneModal .win').removeClass('d-none');
					message = `شما برنده ${Text} شدید`;
					let res = await fetch('/warehouse/fortune/set-prize/', {
						method: 'POST',
						headers: {
							Accept: 'application/json',
							'Content-Type': 'application/json',
						},
						body: JSON.stringify({ RFP: RFP }),
					});
					let info = await res.json();
					if (info.stat == 500) {
						Failed('مشکلی پیش آمده است لطفا بعدا تلاش کنید');
					}
				} else {
					$('#FortuneModal .loose').removeClass('d-none');
					message = `شاید دفعه بعد!`;
				}
				$('.fortune-text').html(message);
				$('#FortuneModal').modal('show');
			}
			$('#FortuneModal').on('hide.bs.modal', function () {
				$('#FortuneModal .win').addClass('d-none');
				$('#FortuneModal .loose').addClass('d-none');
				wheel.css('transform', 'rotate(0deg)');
			});
			function getRotationDegrees(obj) {
				var matrix =
					obj.css('-webkit-transform') ||
					obj.css('-moz-transform') ||
					obj.css('-ms-transform') ||
					obj.css('-o-transform') ||
					obj.css('transform');
				if (matrix !== 'none') {
					var values = matrix.split('(')[1].split(')')[0].split(',');
					var a = values[0];
					var b = values[1];
					var angle = Math.round(Math.atan2(b, a) * (180 / Math.PI));
					// angle += 90
				} else {
					var angle = 0;
				}

				if (angle < 0) angle += 360;
				return angle;
			}
		} else if (x == 300) {
			Failed(
				'امکان استفاده ی مجدد تا فعال شدن گردونه شانس بعدی غیرفعال است'
			);
			setTimeout(() => (window.location.href = '/'), 3000);
		} else {
			Warning(
				'برای استفاده از گردونه شانس ابتدا وارد حساب کاربری خود شوید'
			);
			setTimeout(() => (window.location.href = '/users/register/'), 3000);
		}
	});
});
