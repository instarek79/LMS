var my_array = [1, 2, 3, 4, 5, 6, 7, 8, 9];


$('#filter_type').change(function (e) {
    e.preventDefault();
    filter_type = $(this).val();
    $('#filter_title').text($(this).val());
    $('#output_table').html(`  <tbody>
                    <tr>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                    </tr>
                    <tr>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                    </tr>
                    <tr>
                        <td>0</td>
                        <td>0</td>
                        <td>0</td>
                    </tr>
                </tbody>`);
    if (filter_type == 'Roberts Filter') {
        $('#filter').css({ 'position': 'static' }).addClass('table-bordered');

        $('#filter').html(` 
            <tbody>
                       <tr>
                           <td>1</td>
                           <td>0</td>
                       </tr>
                       <tr>
                           <td>0</td>
                           <td>-1</td>
                       </tr>
                      
                   </tbody>
           `);
    }
    else if (filter_type == 'Prewitt filter') {
        $('#filter').css({ 'position': 'static' }).addClass('table-bordered');
        $('#filter').html(` 
            <tbody>
                       <tr>
                           <td>1</td>
                           <td>1</td>
                           <td>1</td>
                       </tr>
                       <tr>
                        <td>0</td> 
                        <td>0</td> 
                        <td>0</td>
                       </tr>
                       <tr>
                           <td>-1</td>
                           <td>-1</td>
                           <td>-1</td>
                       </tr>
                   </tbody>
           `);
    } else if (filter_type == 'Sobel Filter') {
        $('#filter').css({ 'position': 'static' }).addClass('table-bordered');
        $('#filter').html(` 
            <tbody>
                       <tr>
                           <td>1</td>
                           <td>2</td>
                           <td>1</td>
                       </tr>
                       <tr>
                        <td>0</td> 
                        <td>0</td> 
                        <td>0</td>
                       </tr>
                       <tr>
                           <td>-1</td>
                           <td>-2</td>
                           <td>-1</td>
                       </tr>
                   </tbody>
           `);
    }

    $('.my_table td').each(function (index, element) {
        // element == this
        $(this).text(my_array[index]);

    });
});

function move_to_container_robert(container, index) {
    col = $(container).index();
    row = $(container).parent().index();
    if (isNaN(index)) {
        index = (col) + (row * 3);
    }
    const pos = $(container).position();
    const width = $(container).outerWidth();
    $('#filter').css({ 'position': 'absolute' });
    $('#filter').animate({

        top: (pos.top - 14) + "px",
        left: (pos.left) + "px",
        width: width * 2,
    }).removeClass('table-bordered').addClass('table-borderless');
    $('#filter').find('td').addClass('text-danger text-end pe-4').css('background-color', 'rgba(245, 222, 179, 0.3)')

    var this_value = parseInt($(container).text());
    add_val = isNaN(parseInt($(container).parent().next().find('td').eq(col + 1).text())) ? 0 : parseInt($(container).parent().next().find('td').eq(col + 1).text());
    this_value = this_value - add_val;
    setTimeout(() => {
        // $(container).text(this_value);
        $('#output_table td').eq(index).text(this_value);

    }, 800);


}
function move_to_container_prewit(container, index) {
    col = $(container).index();
    row = $(container).parent().index();
    if (isNaN(index)) {
        index = (col) + (row * 3);
    }
    const pos = $(container).position();
    const width = $(container).outerWidth();
    $('#filter').css({ 'position': 'absolute' });
    $('#filter').animate({

        top: (pos.top - 10) + "px",
        left: (pos.left + (width / 2.33)) + "px",
        width: width * 3,
    }).removeClass('table-bordered').addClass('table-borderless translate-middle ');
    $('#filter').find('td').addClass('text-danger text-end pe-4').css('background-color', 'rgba(245, 222, 179, 0.3)')

    var this_value = parseInt($(container).text());
    if (col > 0) {
        add_val_0 = isNaN(parseInt($(container).parent().prev().find('td').eq(col - 1).text())) ? 0 : parseInt($(container).parent().prev().find('td').eq(col - 1).text());
        sub_val_0 = isNaN(parseInt($(container).parent().next().find('td').eq(col - 1).text())) ? 0 : parseInt($(container).parent().next().find('td').eq(col - 1).text());
    }
    else {
        add_val_0 = 0;
        sub_val_0 = 0;
    }
    add_val_1 = isNaN(parseInt($(container).parent().prev().find('td').eq(col).text())) ? 0 : parseInt($(container).parent().prev().find('td').eq(col).text());
    add_val_2 = isNaN(parseInt($(container).parent().prev().find('td').eq(col + 1).text())) ? 0 : parseInt($(container).parent().prev().find('td').eq(col + 1).text());
    sub_val_1 = isNaN(parseInt($(container).parent().next().find('td').eq(col).text())) ? 0 : parseInt($(container).parent().next().find('td').eq(col).text());
    sub_val_2 = isNaN(parseInt($(container).parent().next().find('td').eq(col + 1).text())) ? 0 : parseInt($(container).parent().next().find('td').eq(col + 1).text());

    console.log(`COL = ${col}  ---  value top_left = ${add_val_0}  --- value_top_middle=${add_val_1}  --- value_top_right=${add_val_2} value bot_left = ${sub_val_0}  --- value_bot_middle=${sub_val_1}  --- value_bot_right=${sub_val_2}`);
    this_value = add_val_1 + add_val_0 + add_val_2 - sub_val_0 - sub_val_1 - sub_val_2;
    setTimeout(() => {
        // $(container).text(this_value);
        $('#output_table td').eq(index).text(this_value);
    }, 800);


}
function move_to_container_sobel(container, index) {
    col = $(container).index();
    row = $(container).parent().index();
    const pos = $(container).position();
    const width = $(container).outerWidth();
    if (isNaN(index)) {
        index = (col) + (row * 3);
    }
    $('#filter').css({ 'position': 'absolute' });
    $('#filter').animate({

        top: (pos.top - 10) + "px",
        left: (pos.left + (width / 2.33)) + "px",
        width: width * 3,
    }).removeClass('table-bordered').addClass('table-borderless translate-middle ');
    $('#filter').find('td').addClass('text-danger text-end pe-4').css('background-color', 'rgba(245, 222, 179, 0.3)')

    var this_value = parseInt($(container).text());
    if (col > 0) {
        add_val_0 = isNaN(parseInt($(container).parent().prev().find('td').eq(col - 1).text())) ? 0 : parseInt($(container).parent().prev().find('td').eq(col - 1).text());
        sub_val_0 = isNaN(parseInt($(container).parent().next().find('td').eq(col - 1).text())) ? 0 : parseInt($(container).parent().next().find('td').eq(col - 1).text());
    }
    else {
        add_val_0 = 0;
        sub_val_0 = 0;
    }
    add_val_1 = isNaN(parseInt($(container).parent().prev().find('td').eq(col).text())) ? 0 : parseInt($(container).parent().prev().find('td').eq(col).text());
    add_val_2 = isNaN(parseInt($(container).parent().prev().find('td').eq(col + 1).text())) ? 0 : parseInt($(container).parent().prev().find('td').eq(col + 1).text());
    sub_val_1 = isNaN(parseInt($(container).parent().next().find('td').eq(col).text())) ? 0 : parseInt($(container).parent().next().find('td').eq(col).text());
    sub_val_2 = isNaN(parseInt($(container).parent().next().find('td').eq(col + 1).text())) ? 0 : parseInt($(container).parent().next().find('td').eq(col + 1).text());

    console.log(`COL = ${col}  ---  value top_left = ${add_val_0}  --- value_top_middle=${add_val_1}  --- value_top_right=${add_val_2} value bot_left = ${sub_val_0}  --- value_bot_middle=${sub_val_1}  --- value_bot_right=${sub_val_2}`);
    this_value = (add_val_1 * 2) + add_val_0 + add_val_2 - sub_val_0 - (sub_val_1 * 2) - sub_val_2;
    setTimeout(() => {
        // $(container).text(this_value);
        $('#output_table td').eq(index).text(this_value);

    }, 800);


}


$('.my_table td').click(function (e) {
    if ($('#filter_type').val() == 'Roberts Filter') {
        move_to_container_robert(this);
    }
    else if ($('#filter_type').val() == 'Prewitt filter') {
        move_to_container_prewit(this);
    }
    else if ($('#filter_type').val() == 'Sobel Filter') {
        move_to_container_sobel(this);
    }
});

$('#start').click(function (e) {
    e.preventDefault();
    var time = 1000;
    $('.my_table td').each(function (index, element) {
        // element == this
        setTimeout(() => {
            if (($('#filter_type').val() == 'Roberts Filter') % index%5!=0 )
                move_to_container_robert(element, index);
            else if ($('#filter_type').val() == 'Prewitt filter') {
                move_to_container_prewit(element, index);
            }
            else if ($('#filter_type').val() == 'Sobel Filter') {
                move_to_container_sobel(element, index);
            }
        }, time);
        time += 1000;
    });
});
