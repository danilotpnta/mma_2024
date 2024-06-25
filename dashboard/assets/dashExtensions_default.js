window.dashExtensions = Object.assign({}, window.dashExtensions, {
    default: {
        function0: function(elements) {
            elements.forEach(function(el) {
                var div = document.getElementById(el.id);
                if (div) {
                    div.style.width = el.value + '%';
                    div.style.transition = 'width 0.3s';
                }
            });
        }

    }
});