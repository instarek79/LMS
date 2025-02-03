let lessons = [{% for keys, lists in chapters.items() %}
'{{keys}}', {% for item in lists %}
'{{item}}', {% endfor %}
{% endfor %}
    ]
$(document).ready(function () {

    nav_height = $('nav').css('height');

    $('#sidebar_right_id').css("min-height", `calc(100vh - ${nav_height}`);
    $('#sidebar_id').css({
        height: `calc(100vh - ${nav_height})`

    });
    $('#document_view_container').css({
        height: `calc(100vh - ${nav_height})`

    });
    // alert(nav_height);
    $(document).on('click', "[name='show_btn_proj']", function () {
        $("[name='show_btn']").each(function (index, element) {
            // element == this
            $(this).removeClass('active');
        });
        $("[name='show_btn_proj']").each(function (index, element) {
            // element == this
            $(this).removeClass('active');
        });
        $(this).addClass('active');
        $('#document_view').html('');
        link = $(this).attr('to');
        $('#document_view').append(
            `<iframe src="${link}" frameborder="0" width='100%' style="height:calc(100vh - ${nav_height} - 20px );"></iframe>`
        )
    });
    $(document).on('click', "[name='show_quiz']", function () {
        $("[name='show_btn']").each(function (index, element) {
            // element == this
            $(this).removeClass('active');
        });
        $("[name='show_btn_proj']").each(function (index, element) {
            // element == this
            $(this).removeClass('active');
        });
        $("[name='show_quiz']").each(function (index, element) {
            // element == this
            $(this).removeClass('active');
        });
        $(this).addClass('active');
        $('#document_view').empty();
        link = $(this).attr('to');

        $('#document_view').load(link, function (response, status, request) {
            this; // dom element

        });
    });


    $(document).on('click', "[name='show_btn']", function (e) {
        lesson_name = $(this).attr('to') == undefined ? $(this).attr('chapter') : $(this).attr('to');

        $('.added_later').remove();
        $('#other_breadcrumbs').append(`<li class="breadcrumb-item active added_later"> ${lesson_name.slice(lesson_name.indexOf(' '))} </li>`);
        e.preventDefault();
        $("[name='show_btn_proj']").each(function (index, element) {
            // element == this
            $(this).removeClass('active');
        });
        $("[name='show_btn']").each(function (index, element) {
            // element == this
            $(this).removeClass('active');
        });
        $(this).addClass('active');
        $('#document_view').empty();
        $('#document_view').show();
        if ($(this).attr('to') != undefined)
            go_to_path = `{{url_for('topics.get_docs',lesson_name='')}}/${encodeURI($(this).attr('to'))}`
        else
            go_to_path = `{{url_for('topics.get_docs',lesson_name='')}}${encodeURI($(this).attr('chapter'))}?domain={{domain|urlencode}}`
        $('#document_view').load(go_to_path, function (response, status, request) {
            this; // dom element

            index = lessons.indexOf(lesson_name);
            if (index > 0 && index < lessons.length - 1) {
                nextItem = lessons[index + 1];
                prevItem = lessons[index - 1];
                $(`<div class="d-flex justify-content-between "  >
                        <a class="icon-link  fs-6 text-center text-decoration-none" name="show_btn" type="button"  to="${prevItem}">
                               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-left" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8"/>
</svg> Prev: ${prevItem.slice(prevItem.indexOf(" "))}
                               
                              </a>
                        <a class="icon-link fs-6 text-center text-decoration-none" name="show_btn" type="button" to="${nextItem}">
                                Next: ${nextItem.slice(nextItem.indexOf(" "))}

                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
                                  </svg>
                              </a></div>`).appendTo('#document_view');
            }
            else if (index == lessons.length - 1) {
                nextItem = lessons[index - 1];
                $(`
                    <div class="d-flex justify-content-start" >
                        <a class="icon-link fs-6 text-decoration-none" name="show_btn" type="button"  to="${nextItem}">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-left" viewBox="0 0 16 16">
  <path fill-rule="evenodd" d="M15 8a.5.5 0 0 0-.5-.5H2.707l3.147-3.146a.5.5 0 1 0-.708-.708l-4 4a.5.5 0 0 0 0 .708l4 4a.5.5 0 0 0 .708-.708L2.707 8.5H14.5A.5.5 0 0 0 15 8"/>
</svg> Prev: ${nextItem.slice(nextItem.indexOf(" "))} 
                              </a></div>`).appendTo('#document_view');
            } else if (index == 0) {
                nextItem = lessons[1];
                $(`<div class="d-flex justify-content-end ">
                        <a class="icon-link fs-6 text-decoration-none" name="show_btn" type="button"  to="${nextItem}">
                                Next: ${nextItem.slice(nextItem.indexOf(" "))}
                               <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-arrow-right" viewBox="0 0 16 16">
                                    <path fill-rule="evenodd" d="M1 8a.5.5 0 0 1 .5-.5h11.793l-3.147-3.146a.5.5 0 0 1 .708-.708l4 4a.5.5 0 0 1 0 .708l-4 4a.5.5 0 0 1-.708-.708L13.293 8.5H1.5A.5.5 0 0 1 1 8"/>
                                  </svg>
                              </a> </div>`).appendTo('#document_view');
            }


        });

        if ($(this).attr('to') == undefined)
            return;
        $.ajax({
            type: "GET",
            url: `/topics/projects/${lesson_name}`,
            data: {},
            contentType: "json",
            success: function (response) {
                $('#projects_list').empty();
                $.each(response, function (indexInArray, Element) {
                    $('#projects_list').append(
                        `  <li class="">
                                <a name="show_btn_proj"  to="${Element.path}"
                                class="btn btn-outline-warning text-start border-0 text-dark p-1"
                                style="font-size: medium;"> ${Element.name}</a>
                                    </li>`
                    );
                });
                response = NaN
            }
        });
        $.ajax({
            type: "GET",
            url: `/topics/applications/${lesson_name}`,
            data: {},
            contentType: "json",
            success: function (response) {
                $('#applications_list').empty();
                $.each(response, function (indexInArray, Element) {
                    $('#applications_list').append(
                        `  <li class="">
                                <a name="show_btn_proj"  to="${Element.path}"
                                class="btn btn-outline-warning text-start border-0 text-dark p-1"
                                style="font-size: medium;"> ${Element.name}</a>
                                    </li>`
                    );
                });
            }
        });
        $.ajax({
            type: "GET",
            url: `/api/quizzes/${lesson_name}`,
            data: {},
            contentType: "json",
            success: function (response) {
                $('#quizes_list').empty();
                $.each(response, function (indexInArray, Element) {
                    $('#quizes_list').append(
                        `  <li class="">
                                <a   to="/questions/view-quiz/${Element.id}"  name="show_quiz"
                                class="btn btn-outline-warning text-start border-0 text-dark p-1"
                                style="font-size: medium;"> ${Element.name}</a>
                                    </li>`
                    );
                });
            }
        });


    });

    $(".toggle_side_left").click(function (e) {
        e.preventDefault();
        $("#sidebar_id").animate({ width: 'toggle' }, 350, function () {
            $('#sidebar_id').toggleClass('d-md-block');
            $('#sidebar_id').toggle();
            $('#show_left').toggleClass('d-none');
        });
        //

    });

    $(".toggle_side_right").click(function (e) {
        // e.preventDefault();
        $("#sidebar_right_id").animate({ width: 'toggle' }, 350, function () {
            $('#sidebar_right_id').toggleClass('d-md-block');
            $('#show_right').toggleClass('d-none');
        });
        //

    });
});
