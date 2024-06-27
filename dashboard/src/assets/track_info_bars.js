window.dash_clientside = Object.assign({}, window.dash_clientside, {
    clientside: {
        resize_track_info_bars: function(songData, prev_styles) {
            console.log(songData)
            console.log(prev_styles)
            var applied_styles = []
            var choice = ""
            
            var elems = [['genre_1', 'genre_2', 'genre_3'], ['key_1', 'key_2', 'key_3']]
        
            for (let i = 0; i < 2; i++) {
                for (let j = 0; j < 3; j++) {
                    var elem = document.getElementsByClassName(elems[i][j])[0]
                    choice = choose(songData[i][1][j])
                    elem.innerHTML = songData[i][0][j] + " " + songData[i][1][j] + "%"
                    if (prev_styles) {
                        if (elem.classList.contains(prev_styles[(i + 1) * (j + 1)])) {
                            elem.classList.remove(prev_styles[(i + 1) * (j + 1)])
                        }
                    }
                    if (i < 1) {
                        elem.style.backgroundColor = songData[0][2][j]
                    }
                    elem.classList.add(choice)
                    applied_styles.push(choice)
                }
            }
            return applied_styles;
        }
    }
});

function choose(value) {
    var choices = ['own-w-5', 'own-w-10', 'own-w-20', 'own-w-30', 'own-w-40', 'own-w-50', 'own-w-60', 'own-w-70', 'own-w-80', 'own-w-84', 'own-w-90', 'own-w-90']
    nearest_number = Math.round(value / 10)
    console.log(value, nearest_number, choices[nearest_number], choices[10])
    return choices[nearest_number];
  }