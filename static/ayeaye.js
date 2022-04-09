function load_kontrollblatt(film, film_insert, film_screenings, kinos){
    //console.log(film);
    //console.log(kinos);
    //console.log(film_insert);
    //console.log(film_screenings);
    $('.titel1').val(film.titel1);
    $('.titel2').val(film.titel2);
    $('.artikel').val(film.artikel);
    $('.land').val(film.land);
    $('.jahr').val(film.jahr);
    $('.min').val(film.min);
    $('.kontrolle').val(film.kontrolle);
    $('.sprache').val(film.sprache);
    $('.fps').val(film.fps);
    $('.fassung').val(film.fassung);
    $('.ut').val(film.ut);
    $('.ut_art').val(film.ut_art);
    $('.preset').val(film.preset);
    $('.kasch').val(film.kasch);
    $('.tonformat').val(film.tonformat);
    $('.toninfo').val(film.toninfo);
    $('.ersterUTnach').val(film.ersterUTnach);
    $('.ersterTONnach').val(film.ersterTONnach);

    $('.presetDB').html(film.presetDB);
    $('.schiene').html(film.schiene);
    $('.Cellregie').html(film.regie);
    $('.filmid').html(film.filmid);
    $('.cpl').html(film.dcpname);
    $('.Celldcpsize').html(film.Celldcpsize);
    $('.playlist').html(film.playlist);
    $('.hinweise_rot').html(film.hinweise_rot);
    $('.Celldcpsize').html(film.Celldcpsize);
    $('.datenbank').html(film.datenbank);
    if (film_insert.Enc == 0){
        $('.enc').html('');
    } else if(film_insert.Enc = 1){
        $('.enc').html('&#x1F512;');
    }

    $(".ScreeningsContainer").html('');
    film_screenings.forEach(obj => {
        //console.log(obj.screening_id);
        var html_string = "";
        kinos.forEach(kino => {
            if (obj.kino == kino.name){
                html_string += kino.name;            
            }
        });
        $(".ScreeningsContainer").append(
            `<div class="Row Screening"> 
                <div class="Cell">
                    ` + html_string + `
                </div>
                <div class="Cell">
                    `+ obj.zeit +`
                </div>
                <div class="Cell cbox">
                    `+obj.ingested+`
                </div>                
                <div class="Cell cbox">
                    `+obj.getestet+`
                </div>
                <div class="Cell vol_sign">
                    ◢
                </div>
                <div class="Cell">
                    `+ obj.soundsetting +`
                </div>
                <div class="Cell keySVG">
                </div>
                <div class="Cell kdm">
                </div>
                </div>
        `
        );
      });
}