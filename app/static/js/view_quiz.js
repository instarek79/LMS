$(document).ready(function () {
    $('#submit_btn').click(function (e) {
        e.preventDefault();
        dataa = {};
        dataa['quiz_id'] = $('#quiz_id').val();
        $("[name='question_container']").each(function (bigindex, element) {
            // element == this
            // console.log('found first loop',bigindex);
            answer = [];
            $(this).find("[name='options']:checked, [name='options'][type='text']").each(function (index, element) {
                // element == this
                // console.log(element);
                answer.push($(this).val());
            });
            dataa[bigindex + 1] = answer

        });
        // console.log(JSON.stringify(data));
        // console.log({ 'name': 'names'});
        $.ajax({
            type: "POST",
            url: "/api/quiz_answer/",
            data: JSON.stringify(dataa),
            contentType: "application/json",
            processData: false,
            success: function (response) {
                console.log(response);
            }, error: function (response) {
                // Handle error response
                console.log(JSON.stringify(dataa));
            },
            dataType: "json"
        });
       
        // #console.log(data);
    });
});