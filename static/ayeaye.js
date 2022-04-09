function load_kontrollblatt(film, film_insert, film_screenings, kinos, keys){
    //console.log(film);
    //console.log(kinos);
    //console.log(film_insert);
    //console.log(film_screenings);
    //console.log(film_keys);
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
        //access a key of this exact screening
        //console.log(keys[kinos[obj.kino].Servernummer]);
        sc_key = keys[kinos[obj.kino].Servernummer];
        if (sc_key){
            key_html = sc_key.Valid_From +'-'+sc_key.Valid_Till;
            sc_enc = '&#x1F512;';
            class_missing = '';

        } else if (film_insert.Enc){
            key_html = '';
            sc_enc = '&#x1F512;';
            class_missing = 'missing';
        } else {
            key_html = '';
            sc_enc = '';
            class_missing = '';

        }
        
        $(".ScreeningsContainer").append(
            `<div class="Row Screening"> 
                <div class="Cell">
                    ` + obj.kino + `
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
                <div class="Cell keySVG `+class_missing+`">
                    `+sc_enc+`
                </div>
                <div class="Cell kdm">
                    `+key_html+`
                </div>
                </div>
        `
        );
        //key symbol greyscale if key is missing
        $('.missing').css("filter","grayscale(100%) invert(100%) opacity(60%)");
      });
}

function search_table() {
    let input = document.getElementById('searchbar').value
    input=input.toLowerCase();
    let x = document.getElementsByClassName('divTableRow');
      
    for (i = 0; i < x.length; i++) { 
        if (!x[i].innerHTML.toLowerCase().includes(input)) {
            x[i].style.display="none";
        }
        else {
            x[i].style.display="table-row";                 
        }
    }
}