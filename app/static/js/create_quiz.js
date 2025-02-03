$(document).ready(function () {
    count = 0
    chosen_questions = []
    $("[name='question_choice']").click(function (e) {
        if (count == 0) $('#questions_cont').addClass('border-bottom border-top border-warning');
        e.preventDefault();
        question_id = $(this).attr('question_id');
        $.get(`/question2/${question_id}`, {},
            function (data, textStatus, jqXHR) {
                $('#questions_cont').append(`<div class='border border-bottom-0 border-warning p-3' ><div class='fs-3 border-bottom border-warning d-flex justify-content-between align-items-center'><div>Question ${count++ + 1}</div> <div class='d-flex'>
                    <label>Marks </label>
                    <input type="text" class="form-control overflow-y-hidden ms-2 mb-1 rounded-0 border-warning text-center" name="marks"  aria-describedby="helpId" style="width:50px;"
                            placeholder="" value='5' min="0" max='100'/>
                    </div> </div>` + data + `</div>`);
            },
        );
        chosen_questions.push(question_id);
        $(this).parent().removeClass('show');
        $(this).remove();

    });

    $(document).on("input", "[name='marks']", function () {
        value = parseInt($(this).val());
        if (value < 0) {
            $(this).val('0');
        }
        if (value > 100) $(this).val('100');
    });
    $('#form_id').submit(function (e) {
        e.preventDefault();
        marks = []
        $("[name='marks']").each(function (index, element) {
            // element == this
            marks.push($(this).val());
        });
        names = $('#formId1').val();

        $.ajax({
            type: "POST",
            url: "/api/quiz/",
            data: JSON.stringify({ 'name': names, 'questions': chosen_questions, 'marks': marks }),
            contentType: "application/json", // Let jQuery handle the contentType
            processData: false, // Prevent jQuery from automatically processing the data
            success: function (response) {
                // Handle success response
                console.log(response);
            },
            error: function (response) {
                // Handle error response
                // console.log(response);
            },
            dataType: "json"
        });
        console.log(marks, chosen_questions);
    });


});