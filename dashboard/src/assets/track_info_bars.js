window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        resize_track_info_bars: function(store, n_clicks) {
            console.log(store)
            console.log(n_clicks)
            var applied_styles = []
            var choice = ""
            var choices = ['w-10', 'w-20', 'w-30', 'w-40', 'w-50', 'w-60', 'w-70', 'w-80', 'w-90']
            var elems = ['genre_1', 'genre_2', 'genre_3', 'key_1', 'key_2', 'key_3']
            for (let i = 0; i < elems.length; i++) {
                var elem = document.getElementsByClassName(elems[i])[0]
                choice = choose(choices)
                if (n_clicks) {
                    if (elem.classList.contains(n_clicks[i])) {
                        elem.classList.remove(n_clicks[i])
                    }
                }
                elem.classList.add(choice)
                applied_styles.push(choice)
            }
            return applied_styles;
        }
    }
});

function choose(choices) {
    var index = Math.floor(Math.random() * choices.length);
    return choices[index];
  }


