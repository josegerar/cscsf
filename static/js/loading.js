//======================================================================
// LOADING
//======================================================================
const Loading = {
    loading: null,
    spin: null,
    wrapper: null,
    backdrop: null,
    hide: function () {
        // Comprueba que exista el HTML
        if (this.loading && this.wrapper && this.spin) {
            // Oculta el HTML de "cargando..." quitando la clase .show
            this.spin.classList.remove('show_loading');

            setTimeout(function () {
                Loading.loading.classList.remove("loading_spinner_custom");
            }, 100);

            setTimeout(function () {
                Loading.wrapper.classList.remove("content_loading_opacity");
            }, 300);

            setTimeout(function () {
                Loading.backdrop.classList.remove("loading-backdrop");
            }, 500);
        }

    },
    show: function () {
        if (this.loading && this.wrapper && this.spin && this.backdrop) {
            //this.spin.style.top = "calc(50vh - var(--scrollbar-height));"
            //this.spin.style.left = "calc(50vw - var(--scrollbar-width));"
            this.spin.style.setProperty('top', 'calc(var(--scrollbar-height))');
            this.spin.style.setProperty('left', 'calc(var(--scrollbar-width))');
            this.loading.classList.add('loading_spinner_custom');
            this.backdrop.classList.add('loading-backdrop');
            this.wrapper.classList.add('content_loading_opacity');
            this.spin.classList.add('show_loading');
        } else {
            this.init(function () {
                Loading.show();
            })
        }
    },
    init: function (callback) {
        /* Comprobar que el HTML esté cargadas */
        if (document.readyState === "loaded" ||
            document.readyState === "interactive" ||
            document.readyState === "complete") {
            this.initParameters();
            callback();
        } else {
            document.addEventListener('DOMContentLoaded', function () {
                Loading.initParameters();
                callback();
            });
        }
    },
    initParameters: function () {
        this.loading = document.body;

        this.spin = document.createElement('div');
        this.spin.classList.add("spin_custom");
        this.loading.appendChild(this.spin);

        this.backdrop = document.createElement('div');
        this.backdrop.classList.add("loading-backdrop");
        this.loading.appendChild(this.backdrop);

        this.wrapper = this.loading.querySelector('.main-container-load');

    },
    _calculateScrollbarWidth: function () {
        document.documentElement.style.setProperty('--scrollbar-width', ((document.body.clientWidth)/2) + "px");
        document.documentElement.style.setProperty('--scrollbar-height', ((document.body.clientHeight)/2) + "px");
    }
}

// recalculate on resize
window.addEventListener('resize', Loading._calculateScrollbarWidth, false);
// recalculate on dom load
document.addEventListener('DOMContentLoaded', Loading._calculateScrollbarWidth, false);
// recalculate on load (assets loaded as well)
window.addEventListener('load', Loading._calculateScrollbarWidth);
