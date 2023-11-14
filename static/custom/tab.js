'use strict';
function onYouTubeIframeAPIReady() {
	THEME.Video.loadVideos();
}
(window.THEME = {}),
	(function (t) {
		var e = function () {
				var e = t(
					'<div style="width:100px;height:100px;overflow:scroll;visibility: hidden;"><div style="height:200px;"></div>'
				);
				s.append(e);
				var a = e[0].offsetWidth - e[0].clientWidth;
				return t(e).remove(), a;
			},
			a = function () {
				var e = 0.01 * window.innerHeight;
				t('html').css('--vh', e + 'px'),
					t('html').css('--scrollW', c + 'px');
			},
			i = function (t, e) {
				return Math.floor(Math.random() * (e - t + 1) + t);
			};
        (THEME.header = {
            init: function () {
                    this.megaMenu()
            },
            megaMenu: function () {
                (THEME.megamenu = {
                    defaults: {
                        header: '.hdr',
                        menu: '.mmenu-js',
                        submenu: '.mmenu-submenu',
                        toggleMenu: '.toggleMenu',
                        megaDropdn: '.mmenu-item--mega',
                        titleHeight: 50,
                    },
                    init: function (e) {
                        t.extend(this.defaults, e),
                            t(this.defaults.menu).length &&
                                (this._handlers(this),
                                t(this.defaults.menu).find('.menu-label')
                                    .length &&
                                    t(this.defaults.menu).addClass(
                                        'mmenu--withlabels'
                                    ));
                    },
                    _handlers: function (e) {
                        var a = t(e.defaults.menu),
                            i = e.defaults.submenu,
                            n = t(e.defaults.submenu, a),
                            d = t(e.defaults.header),
                            f =
                                (e.defaults.vertical,
                                t(e.defaults.headerCart)),
                            p = f.find(e.defaults.headerCartToggleBtn),
                            m = f.find(e.defaults.headerCartDropdn),
                            g = t(e.defaults.dropdn, d),
                            v = void 0;
                        a
                            .on(
                                'mouseenter.mmenu',
                                u + '> a,' + h + '> a',
                                function () {
                                    var e = t(this);
                                    v = setTimeout(function () {
                                        (n = e.next(i)),
                                            (function (e, i) {
                                                if (
                                                    a.hasClass(
                                                        'mmenu--vertical'
                                                    )
                                                )
                                                    return !1;
                                                if (i.length) {
                                                    var o = s.hasClass(
                                                        'has-sticky'
                                                    )
                                                        ? e -
                                                        t(
                                                                '.hdr-content-sticky'
                                                        ).outerHeight()
                                                        : e -
                                                        i.prev().offset()
                                                                .top -
                                                        i
                                                                .prev()
                                                                .outerHeight();
                                                    i.children(
                                                        ':first'
                                                    ).css({
                                                        'max-height':
                                                            o + 'px',
                                                    });
                                                }
                                            })(o.height(), n),
                                            n.scrollTop(0),
                                            e
                                                .parent('li')
                                                .addClass('hovered'),
                                            n
                                                .find('.mmenu-col')
                                                .each(function (e) {
                                                    var a = t(this);
                                                    anime({
                                                        targets: a[0],
                                                        opacity: [0, 1],
                                                        translateY: [
                                                            '80px',
                                                            '0',
                                                        ],
                                                        translateZ: 0,
                                                        translateX: 0,
                                                        easing: 'cubicBezier(0.165, 0.84, 0.44, 1)',
                                                        duration: 650,
                                                        delay: 100 * e,
                                                        complete:
                                                            function () {
                                                                a.css({
                                                                    transform:
                                                                        'none',
                                                                });
                                                            },
                                                    });
                                                }),
                                            m.hasClass('opened') &&
                                                p.trigger('click'),
                                            g.each(function () {
                                                var e = t(this);
                                                e.hasClass('is-hovered') &&
                                                    t('>a', e).trigger(
                                                        'click'
                                                    );
                                            });
                                    }, 200);
                                }
                            )
                            .on(
                                'mouseleave.mmenu',
                                u + ',' + h,
                                function () {
                                    var e = t(this);
                                    clearTimeout(v),
                                        n.each(function () {
                                            t(this).css({
                                                'max-height': '',
                                            });
                                        }),
                                        e.removeClass('hovered');
                                }
                            ),
                            c.on('click', function (t) {
                                var e = this;
                                d.toggleClass('open'),
                                    e.toggleClass('open'),
                                    a
                                        .addClass('disable')
                                        .delay(1e3)
                                        .queue(function () {
                                            e.removeClass(
                                                'disable'
                                            ).dequeue();
                                        }),
                                    t.preventDefault();
                            }),
                            t('li', n)
                                .on('mouseenter', function () {
                                    var e = t(this).addClass('hovered');
                                    if (t('> a .mmenu-preview', e).length) {
                                        var a = e.closest('ul'),
                                            i = t('.mmenu-preview', e);
                                        a.css({
                                            'min-width': '',
                                            overflow: '',
                                        }),
                                            a.css({
                                                'min-width': 454,
                                                overflow: 'hidden',
                                            }),
                                            a.append(i.clone());
                                    }
                                    if (
                                        t('> .submenu-link-image', e).length
                                    ) {
                                        var n = t(
                                                '> .submenu-link-image',
                                                e
                                            ),
                                            d = s.hasClass('rtl')
                                                ? n.offset().left >= 0
                                                : n.offset().left +
                                                        n.width() <=
                                                l,
                                            c =
                                                r +
                                                o.scrollTop() -
                                                (n.offset().top +
                                                    n.outerHeight());
                                        d
                                            ? n.removeClass('to-right')
                                            : n.addClass('to-right'),
                                            c < 0 &&
                                                n.css({
                                                    'margin-top': c + 'px',
                                                });
                                    } else if (t('ul', e).length) {
                                        var u,
                                            h,
                                            f = t('.mmenu-submenu', e)
                                                .length
                                                ? t('.mmenu-submenu', e)
                                                : t('ul:first', e);
                                        e.closest('.mmenu-item--mega')
                                            .length &&
                                            e
                                                .parent()
                                                .hasClass('submenu-list') &&
                                            (s.hasClass('rtl'),
                                            f.css({
                                                top:
                                                    e.offset().top -
                                                    e
                                                        .closest(
                                                            '.mmenu-submenu'
                                                        )
                                                        .offset().top,
                                                left:
                                                    e.offset().left -
                                                    f.outerWidth(),
                                            })),
                                            (u = s.hasClass('rtl')
                                                ? f.offset().left >= 0
                                                : f.offset().left +
                                                        f.width() <=
                                                l),
                                            (h =
                                                r +
                                                o.scrollTop() -
                                                (f.offset().top +
                                                    f.outerHeight())),
                                            u
                                                ? e.removeClass('to-right')
                                                : e.addClass('to-right'),
                                            h < 0 &&
                                                f.css({
                                                    'margin-top': h + 'px',
                                                });
                                    }
                                })
                                .on('mouseleave', function () {
                                    var e = t('.mmenu-submenu', this).length
                                            ? t('.mmenu-submenu', this)
                                            : t('ul:first', this),
                                        a = t(this)
                                            .removeClass('to-right')
                                            .removeClass('hovered');
                                    if (
                                        (t(
                                            '.submenu-link-image',
                                            t(this)
                                        ).removeClass('to-right'),
                                        t('> a .mmenu-preview', a).length)
                                    ) {
                                        var i = a.closest('ul');
                                        i.css({
                                            'min-width': '',
                                            overflow: '',
                                        }),
                                            i
                                                .find('>.mmenu-preview')
                                                .remove();
                                    }
                                    e.css({ 'margin-top': '' }),
                                        a.closest('.sub-level').length ||
                                            e
                                                .closest('.mmenu-submenu')
                                                .removeClass(
                                                    'mmenu--not-hide'
                                                )
                                                .css({
                                                    'padding-left': '',
                                                }),
                                        t('.submenu-link-image', a)
                                            .length &&
                                            t('.submenu-link-image', a).css(
                                                { 'margin-top': '' }
                                            );
                                });
                    },
                }),
                    THEME.megamenu.init();
            }
            }),
        (THEME.documentReady = {
            init: function () {
                s.addClass('ready'),
                    // THEME.header.mobileMenu('.mobilemenu'),
                    THEME.header.init()
        }
        });
var s = t('body'),
o = t(window),
n = t(document),
l = window.innerWidth || o.width(),
r = window.innerHeight || o.height(),
d = void 0,
c = e(),
u = !1,
h = 480,
f = 768,
p = 992,
m = 1200,
g = 1025,
v = 1025,
b = l < g,
y = s.hasClass('template-product'),
C = s.hasClass('template-collection');
a()
THEME.documentReady.init()
})(jQuery);

