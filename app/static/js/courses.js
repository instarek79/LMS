

function update_student_list(course_id) {
    $.get(`/api/courses/get_students/${course_id}`, {},
        function (data, textStatus, jqXHR) {
            $('#add_container').empty().html(`
                  <a name="" id="" class="btn btn-warning  rounded-bottom-0  " role="button"
                            data-bs-toggle="modal" data-bs-target="#addstudentmodal"><i class="bi bi-plus-lg "></i>
                            <span class="d-none d-md-inline">Add
                                Student </span> </a>
                `);

            $('#table_title').text(`Course: Students`);
            $('#table_head').html(`
                   <tr class="justify-content-evenly">
                            <th scope="col" style="width: max-content">First name</th>
                            <th scope="col" style="width: max-content">Last name</th>
                            <th scope="col" style="width: max-content">Email</th>
                            <th scope="col" style="width: max-content">Actions</th>
                        </tr>`);
            $('tbody').empty();
            $.each(data, function (indexInArray, student) {
                $('tbody').append(`
                <tr>
                    <td>${student.first_name}</td>
                    <td>${student.last_name}</td>
                    <td>${student.email}</td>
                    <td>
                        <button  class="btn btn-outline-secondary  border-0 delete-btn" course_id="${course_id}" student_id="${student.id}">
                        <i class="bi bi-x-lg">
                        </i>
                        </button>
                    </td>
                </tr>
                `);
            });
        },
        "json"
    );
}
function reset_add_quiz() {
    $('#add_quiz').html(` <div class="row justify-content-center">
                        <div class="col-12 col-md-8  border rounded-3 p-3 ">
                            <div class="form-floating mb-3">
                                <input type="text" name="name" id="quiz_name" class="form-control form-control-lg"
                                    placeholder="name" required>
                                <label for="quiz_name">Quiz Name</label>
                            </div>
                            <div class="h3 mb-3 d-flex flex-wrap justify-content-around">
                                <div> Questions Count: <span id="question_count">1</span>
                                </div>
                                <div>
                                    Total Marks: <span id="total_mark">5</span>
                                </div>
                            </div>
                            <div id="question_container" class="mb-3 pt-3 border-top ">
                                <div class="border m-3  p-0  question-div">
                                    <div class="d-flex m-1 justify-content-end">
                                        <button type="button" id="delete_question" class="btn btn-close">
                                    </div>
                                    <div class="p-3 pt-0">


                                        <div class="input-group mb-3">
                                            <div class="form-floating  w-75">
                                                <input type="text" name="text" class="form-control" placeholder="" required>
                                                <label>Question</label>
                                            </div>
                                            <div class="form-floating w-25 ">
                                                <input type="number" step="1" name="mark" class="form-control"
                                                    placeholder="" value="5" required>
                                                <label>Marks</label>
                                            </div>
                                        </div>
                                        <div class="h4">
                                            Only mark the correct answer:
                                        </div>
                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio"
                                                    value="1" name="correct_option_1" required>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option A"
                                                name="option_1" required>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio"
                                                    value="2" name="correct_option_1" required>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option B"
                                                name="option_2" required>
                                        </div>
                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio"
                                                    value="3" name="correct_option_1" required>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option C"
                                                name="option_3" required>
                                        </div>
                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio"
                                                    value="4" name="correct_option_1" required>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option D"
                                                name="option_4" required>
                                        </div>

                                    </div>
                                </div>
                            </div>
                            <div class="d-grid px-4">
                                <button type="button" id="add_question"
                                    class="btn btn-outline-light text-black border-black">
                                    <i class="bi bi-plus-lg"></i> Add New Question
                                </button>
                            </div>

                        </div>
                    </div>`);
}
function update_correct_question() {
    $(".correct-option").each(function (index, element) {
        // element == this
        count = parseInt(index / 4) + 1;
        $(this).attr("name", "correct_option_" + count);
    });
}
function update_correct_question() {
    $("question_container2 > .correct-option").each(function (index, element) {
        // element == this
        count = parseInt(index / 4) + 1;
        $(this).attr("name", "correct_option_" + count);
    });
}
function update_marks() {
    total_marks = 0;
    $("question_container > [name='mark']").each(function (index, element) {
        // element == this
        total_marks += isNaN(parseInt(element.value)) ? 0 : parseInt(element.value);
    });
    $('#total_mark').text(total_marks);
}function update_marks_2() {
    total_marks = 0;
    $("question_container2 > [name='mark']").each(function (index, element) {
        // element == this
        total_marks += isNaN(parseInt(element.value)) ? 0 : parseInt(element.value);
    });
    $('#total_mark').text(total_marks);
}
function update_course_list() {
    $.get("/api/courses/get_managed_course", {},
        function (data, textStatus, jqXHR) {
            $('#table_title').text('Courses');
            $('#table_head').html(`
            <tr class="justify-content-evenly">
                                    <th scope="col" style="width: max-content">img</th>
                                    <th scope="col" style="width: max-content">Name</th>
                                    <th scope="col" style="width: max-content">Description</th>
                                    <th scope="col" style="width: max-content">Topics</th>
                                    <th scope="col" style="width: max-content" class="text-nowrap">Number of students</th>
                                    <th scope="col" style="width: max-content" class="text-nowrap">Number of quizzes </th>
                                    <th scope="col" style="width: 5%;">Actions</th>
                                </tr> 
            
            `);
            $('#add_course_modal').empty();
            $.each(data, function (indexInArray, valueOfElement) {
                $('#add_course_modal').append(`
                <tr>
                    <td><img src="${valueOfElement.image}" alt="course img" class="img-fluid rounded-circle  "
                                    style="height: 30px;"></td>
                    <td>${valueOfElement.name}</td>
                    <td>${valueOfElement.description}</td>
                    <td>${valueOfElement.topics.length}</td>
                    <td>${valueOfElement.students.length}</td>
                    <td>${valueOfElement.quizzes.length}</td>
                    <td>
                    <div class="dropdown open">
                                    <button class="btn btn-outline-secondary border-0 " type="button" id="triggerId"
                                        data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bi bi-three-dots-vertical"></i>
                                    </button>
                                    <div class="dropdown-menu" aria-labelledby="triggerId">
                                        <button class=" dropdown-item student-btn" href="#"
                                            course_id="${valueOfElement.id}">Students</button>
                                        <button class="dropdown-item topic-btn" href="#"
                                            course_id="${valueOfElement.id}">Topics</button>
                                        <button class="dropdown-item quiz-btn" href="#"
                                            course_id="${valueOfElement.id}">Quizzes</button>
                                        
                                        <button class="dropdown-item delete-btn" href="#"
                                            course_id="${valueOfElement.id}">Delete</button>

                                    </div>
                                </div>
                            </td>
                </tr>`
                );
            });
        },
        "json"
    );
}

function update_quizzes_list(course_id) {
    $.ajax({
        type: "GET",
        url: `/api/quizzes/from_course/${course_id}`,
        data: {},
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            $('#table_title').text(`Course: Quizzes`);
            $('tbody').empty();
            $('#add_container').empty().html(`
                <a name="" id="" class="btn btn-warning  rounded-bottom-0  " role="button"
                          data-bs-toggle="modal" data-bs-target="#addquizmodal"><i class="bi bi-plus-lg "></i>
                          <span class="d-none d-md-inline">Add
                              Quiz </span> </a>
              `);
            $('#table_head').html(`
            <tr class="justify-content-evenly">
                            <th scope="col" style="width: max-content">Number</th>
                            <th scope="col" style="width: max-content">Name</th>
                            <th scope="col" style="width: max-content">Marks (Total)</th>     
                            <th scope="col" style="width: max-content">Date </th>     

                            <th scope="col" style="width: max-content">Actions </th>     

                            </tr>
            `);
            $.each(data, function (indexInArray, quiz) {
                $('tbody').append(`
                <tr>
                    <td>${indexInArray + 1}</td>
                    <td>${quiz.name}</td>
                    <td>${quiz.marks}</td>
                    <td>${quiz.date}</td>
                    <td>
                    <div class="dropdown open">
                                    <button class="btn btn-outline-secondary border-0 " type="button" id="triggerId"
                                        data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                        <i class="bi bi-three-dots-vertical"></i>
                                    </button>
                                    <div class="dropdown-menu" aria-labelledby="triggerId">
                                        <button class="dropdown-item edit-btn" href="#"
                                            quiz_id="${quiz.id}">Edit</button>
                                        <button class="dropdown-item delete-btn" course_id=${course_id} href="#"
                                            quiz_id="${quiz.id}">Delete</button>

                                    </div>
                                </div>
                            </td>
                </tr>
                `);
            });

        }
    }).always(function () {

    });
}

function update_topic_list(course_id) {
    $.ajax({
        type: "GET",
        url: `/api/courses/get_topics/${course_id}`,
        data: {},
        dataType: "json",
        contentType: "application/json",
        success: function (data) {
            $('#table_title').text(`Course: Topics`);
            $('tbody').empty();
            $('#table_head').html(`
            <tr class="justify-content-evenly">
                            <th scope="col" style="width: max-content">Number</th>
                            <th scope="col" style="width: max-content">Name</th>
                            <th scope="col" style="width: max-content">Actions</th>     
                        </tr>
            `);
            $.each(data, function (indexInArray, topic) {

                $('tbody').append(`
                <tr>
                    <td>${indexInArray + 1}</td>
                    <td>${topic.name}</td>
                    <td>
                        <div class="dropdown ">
                            <button class="btn btn-outline-secondary border-0 " type="button" id="triggerId"
                                            data-bs-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
                                            <i class="bi bi-three-dots-vertical"></i>
                            </button>
                            <div class="dropdown-menu" aria-labelledby="triggerId">
                                <button class="dropdown-item edit-btn" href="#"
                                                topic_id="${topic.id}"">Edit</button>
                                <button class="dropdown-item delete-topic-btn" href="#"
                                                topic_id="${topic.id}"">Delete</button>

                            </div>
                        </div>
                    </td>
                    
                </tr>
                `);
            });
        }
    }).always(function () {
        get_flash();
    });

}
$(document).ready(function () {
    // Get today's date
    const today = new Date();
    // Add one day to get tomorrow
    today.setDate(today.getDate() + 2);
    // Set hours, minutes, seconds, and milliseconds to zero for midnight
    today.setHours(0, 0, 0, 0);
    // Format the date to 'YYYY-MM-DDTHH:MM'
    const formattedDate = today.toISOString().slice(0, 16);
    // Set the min attribute of the input
    document.getElementById('quiztime').setAttribute('min', formattedDate);
    
    let user_id = 0;
    var topic_id;
    var student_id;
    var course_id;
    var quiz_id;
    $('#add_student').submit(function (e) {
        e.preventDefault();
        data = $(this).serializeArray();
        data = JSON.stringify(data);
        $.ajax({
            type: "PUT",
            url: "/api/courses/add_students",
            data: data,
            dataType: "json",
            contentType: "application/json",  // Set to false for FormData
            success: function (data) {
                const myModal2 = bootstrap.Modal.getInstance($('#addstudentmodal'));
                myModal2.hide();
                $("#students_select").empty()
                update_student_list(course_id);
            }

        }).always(function () {
            get_flash();
        });

    });
    $.get("/api/user/get_id", {},
        function (data, textStatus, jqXHR) {
            user_id = data['id'];
        },
    );

    // $(document).on('click','#add_student', function () {

    // });
    $(document).on('click', '.student-btn', function (e) {
        e.preventDefault();
        course_id = $(this).attr('course_id');
        initializeSelect2();
        $('#course_id').val(course_id);
        update_student_list(course_id);
    });
    $('.table-responsive').on('show.bs.dropdown', function () {
        $('.table-responsive').css("overflow", "inherit");
    });

    $('.table-responsive').on('hide.bs.dropdown', function () {
        $('.table-responsive').css("overflow", "auto");
    })

    $(document).on('click', '.edit-btn', function (e) {
        e.preventDefault();
        topic_id = $(this).attr('topic_id');
        quiz_id = $(this).attr('quiz_id');
        if (!isNaN(topic_id)) {
            $.ajax({
                type: "GET",
                url: "/api/topics/" + `?topic_id=${topic_id}`,
                data: false,
                dataType: "json",
                contentType: "application/json",
                success: function (response) {
                    $('#EditTopicName').val(response.name);
                    // Set the new data
                    const domEditableElement = document.querySelectorAll('.ck-editor__editable_inline')[1];
                    const editorInstance = domEditableElement.ckeditorInstance;
                    editorInstance.setData(response.content);


                }
            });
            const myModal = new bootstrap.Modal('#EditTopicModal');
            myModal.show();
        }
        else if (!isNaN(quiz_id)) {
            $.ajax({
                type: "GET",
                url: "/api/quizzes/" + `?quiz_id=${quiz_id}`,
                data: false,
                dataType: "json",
                contentType: "application/json",
                success: function (response) {
                    question_count_edit = response.questions.length;
                    $('#edit_name').val(response.name);
                    $('#question_container2').empty();
                    $('#total_mark_edit').text(response.marks);
                    $('#question_count_edit').text(response.questions.length);
                    $('#edit_quiz_time').val(response.date);
                    $.each(response.questions, function (indexInArray, question) {
                        $('#question_container2').append(`
                              <div class="border m-3  p-0  question-div">
                                    <div class="d-flex m-1 justify-content-end">
                                        <button type="button" id="delete_question2" class="btn btn-close">
                                    </div>
                                    <div class="p-3 pt-0">


                                        <div class="input-group mb-3">
                                            <div class="form-floating  w-75">
                                                <input type="text" name="text" class="form-control" placeholder="" value=${question.question.text} required>
                                                <label>Question</label>
                                            </div>
                                            <div class="form-floating w-25 ">
                                                <input type="number" step="1" name="mark" class="form-control"
                                                    placeholder="" value="${question.marks}" required>
                                                <label>Marks</label>
                                            </div>
                                        </div>
                                        <div class="h4">
                                            Only mark the correct answer:
                                        </div>
                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio"
                                                    value="1" name="correct_option_${indexInArray + 1}" required ${question.question.correct_option === 1 ? 'checked' : ''}>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option A"
                                                name="option_1" required value="${question.question.option_1}">
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio"
                                                    value="2" name="correct_option_${indexInArray + 1}" required ${question.question.correct_option === 2 ? 'checked' : ''}>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option B"
                                                name="option_2" required value="${question.question.option_2}">
                                        </div>
                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio"
                                                    value="3" name="correct_option_${indexInArray + 1}" required ${question.question.correct_option === 3 ? 'checked' : ''}>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option C"
                                                name="option_3" required value="${question.question.option_3}">
                                        </div>
                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio"
                                                    value="4" name="correct_option_${indexInArray + 1}" required ${question.question.correct_option === 4 ? 'checked' : ''}>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option D"
                                                name="option_4" required value="${question.question.option_4}">
                                        </div>

                                    </div>
                                </div>
                            `);
                    });
                    const myModal = new bootstrap.Modal('#edit_quiz_modal');
                    myModal.show();
                }
            });

        }


        //open addtopicmodal
    });
    $('#edit_topic').submit(function (e) {
        e.preventDefault();
        const domEditableElement = document.querySelectorAll('.ck-editor__editable_inline')[1];
        const editorInstance = domEditableElement.ckeditorInstance;
        content = editorInstance.getData();
        data = {
            name: $('#EditTopicName').val(),
            content: content,
        }
        data = JSON.stringify(data);
        $.ajax({
            type: "PUT",
            url: "/api/topics/" + `?topic_id=${topic_id}`,
            data: data,
            dataType: "json",
            contentType: "application/json",
            success: function (response) {
                const myModal2 = bootstrap.Modal.getInstance($('#EditTopicModal'));
                myModal2.hide();

            }
        }).always(function () {
            get_flash();
        });
    });

    $('li>a.nav-link').click(function (e) {
        // e.preventDefault();
        $('li>a.nav-link').removeClass('active text-black').addClass('text-white');
        $(this).removeClass('text-white').addClass('active text-black');

    });

    $('#add_course').submit(function (e) {
        e.preventDefault();
        $.ajax({
            type: "POST",
            url: "/api/courses/add",
            data: new FormData(this),
            dataType: "json",
            contentType: false,  // Set to false for FormData
            processData: false,
            success: function (data) {
                update_course_list();
                const myModal2 = bootstrap.Modal.getInstance($('#exampleModal'));
                myModal2.hide();
            }

        }).always(function () {
            get_flash();
        });



    });

    $('#courses_view').click(function (e) {
        e.preventDefault();

        update_course_list();
        course_id = NaN;
        topic_id = NaN;
        quiz_id = NaN;
        student_id = NaN;


    });

    $("#search_field").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#add_course_modal tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
    $(document).on('click', '.delete-btn', function (e) {
        e.preventDefault();
        student_id = $(this).attr('student_id');
        quiz_id = $(this).attr('quiz_id');
        course_id = $(this).attr('course_id');
        const myModalAlternative = new bootstrap.Modal('#are_you_sure_modal');
        myModalAlternative.show();

    });
    $(document).on('click', '.delete-topic-btn', function (e) {
        e.preventDefault();
        topic_id = $(this).attr('topic_id');
        if (!isNaN(topic_id)) {
            const myModalAlternative = new bootstrap.Modal('#are_you_sure_modal');
            myModalAlternative.show();
        }

    });
    $(document).on('click', '.quiz-btn', function (e) {
        e.preventDefault();
        course_id = $(this).attr('course_id');
        update_quizzes_list(course_id);

    });
    $('#are_sure_btn').click(function (e) {
        e.preventDefault();
        if (!isNaN(student_id) && !isNaN(course_id)) {
            $.ajax({
                type: "DELETE",
                url: "/api/courses/remove_student_from_course",
                data: JSON.stringify({
                    "student_id": student_id,
                    "course_id": course_id
                }),
                dataType: "json",
                contentType: "application/json",  // Set to false for FormData
                success: function (data) {
                    const myModalAlternative = bootstrap.Modal.getInstance($('#are_you_sure_modal'));
                    myModalAlternative.hide();
                    update_student_list(course_id);
                }
            }).always(function () {
                get_flash();
                return;
            });

            student_id = NaN;
        }
        else if (!isNaN(topic_id) && !isNaN(course_id) && isNaN(student_id) && isNaN(quiz_id)) {
            $.ajax({
                type: "DELETE",
                url: "/api/courses/remove_topic_from_course",
                data: JSON.stringify({
                    "topic_id": topic_id,
                    "course_id": course_id
                }),
                dataType: "json",
                contentType: "application/json",  // Set to false for FormData
                success: function (data) {
                    const myModalAlternative = bootstrap.Modal.getInstance($('#are_you_sure_modal'));
                    myModalAlternative.hide();
                    update_topic_list(course_id);
                }
            }).always(function () {
                get_flash();
            });

            topic_id = NaN;
        }
        else if (!isNaN(course_id) && !isNaN(quiz_id) && isNaN(student_id) && isNaN(topic_id)) {
            $.ajax({
                type: "DELETE",
                url: "/api/quizzes/",
                data: JSON.stringify({
                    "id": quiz_id,
                }),
                dataType: "json",
                contentType: "application/json",  // Set to false for FormData
                success: function (data) {
                    const myModalAlternative = bootstrap.Modal.getInstance($('#are_you_sure_modal'));
                    myModalAlternative.hide();
                    update_quizzes_list(course_id);
                }
            }).always(function () {
                get_flash();
            });

            quiz_id = NaN;
        }
        else if (isNaN(topic_id) && !isNaN(course_id) && isNaN(student_id) && isNaN(quiz_id)) {
            $.ajax({
                type: "DELETE",
                url: `/api/courses/delete/${course_id}`,
                data: NaN,
                dataType: "json",
                contentType: "application/json",  // Set to false for FormData
                success: function (data) {
                    const myModalAlternative = bootstrap.Modal.getInstance($('#are_you_sure_modal'));
                    myModalAlternative.hide();
                    update_student_list(course_id);
                }
            }).always(function () {
                update_course_list();
                get_flash();
            });
            course_id = NaN;
        }
        else if (isNaN(topic_id) && !isNaN(course_id) && isNaN(student_id) && !isNaN(quiz_id)) {
            $.ajax({
                type: "DELETE",
                url: `/api/quizzes/`,
                data: JSON.stringify({
                    "id": quiz_id,
                }),
                dataType: "json",
                contentType: "application/json",  // Set to false for FormData
                success: function (data) {
                    const myModalAlternative = bootstrap.Modal.getInstance($('#are_you_sure_modal'));
                    myModalAlternative.hide();
                    update_quizzes_list(course_id);
                }
            }).always(function () {
                get_flash();
            });
            quiz_id = NaN;
        }


    });
    function initializeSelect2() {
        $('#students_select').select2({
            theme: "bootstrap-5",
            width: $(this).data('width') ? $(this).data('width') : $(this).hasClass('w-100') ? '100%' : 'style',
            dropdownParent: $("#addstudentmodal"),
            allowClear: true,
            ajax: {
                url: `/api/courses/get_students_not/${course_id}`,
                dataType: 'json',
                delay: 250,  // Delay in ms before sending the request (for debouncing)
                processResults: function (data) {
                    // Map the results to the format Select2 expects
                    return {
                        results: data.map(student => ({
                            id: student.id,  // The value for the option
                            text: `${student.first_name} ${student.last_name}`  // The text to display
                        }))
                    };
                },
                cache: true
            },
            placeholder: 'Select a student',  // Placeholder for the dropdown
        });
    }


    $(document).on('click', '.topic-btn', function (e) {
        e.preventDefault();
        course_id = $(this).attr('course_id');
        $('#add_container').html(`  <a name="" id="" class="btn btn-warning  rounded-bottom-0  " role="button"
            data-bs-toggle="modal" data-bs-target="#TopicModal"><i class="bi bi-plus-lg "></i>
            <span class="d-none d-md-inline">Add Topics </span> </a>`);
        update_topic_list(course_id);
    });

    $('#add_topic').submit(function (e) {
        e.preventDefault();
        form=this;
        formData = new FormData(this);
        var data = {};
        formData.forEach(function (value, key) {
            data[key] = value;
        });

        const domEditableElement = document.querySelector('.ck-editor__editable_inline');
        const editorInstance = domEditableElement.ckeditorInstance;
        data['content'] = editorInstance.getData();
        data = JSON.stringify(data);
        $.ajax({
            type: "POST",
            url: `/api/courses/add_topic/${course_id}`,
            data: data,
            dataType: "json",
            contentType: "application/json",  // Set to false for FormData
            success: function (data) {
                update_topic_list(course_id);
                const myModal2 = bootstrap.Modal.getInstance($('#TopicModal'));
                myModal2.hide();
                form.reset();
                editorInstance.setData('');
            }
        }).always(function () {
            get_flash();
        });
    });
    $('#add_quiz').submit(function (e) {
        e.preventDefault();
        // data = $(this).serializeArray();
        // data = JSON.stringify(data);
        data = new FormData(this);
        data.append('course_id', course_id);
        $.ajax({
            type: "POST",
            url: "/api/quizzes",
            data: data,
            dataType: "json",
            contentType: false,  // Set to false for FormData
            processData: false,

            success: function (data) {

                const myModal2 = bootstrap.Modal.getInstance($('#addquizmodal'));
                myModal2.hide();

                update_quizzes_list(course_id);
                reset_add_quiz();
            }
        }).always(function () {
            get_flash();
        });
    });
    $(document).on("click", "#delete_question", function () {
        if (question_count > 1) {
            $(this).parent().parent().remove();
            question_count--;
            $('#question_count').text(question_count);
            update_marks();
            update_correct_question();

        }
    });
    $(document).on("click", "#delete_question2", function () {
        if (question_count_edit > 1) {
            $(this).parent().parent().remove();
            question_count--;
            $('#question_count').text(question_count);
            update_marks_2();
            update_correct_question_2();

        }
    });
    question_count = 1;
    question_count_edit = 1;
    $('#add_question').click(function (e) {
        e.preventDefault();
        question_count++;

        $('#question_container').append(
            `
             <div class="border m-3  p-0  question-div">
                                    <div class="d-flex m-1 justify-content-end">
                                        <button type="button" id="delete_question" class="btn btn-close">
                                    </div>
                                    <div class="p-3 pt-0">


                                        <div class="input-group mb-3">
                                            <div class="form-floating  w-75">
                                                <input type="text" name="text" class="form-control" placeholder="" required>
                                                <label>Question</label>
                                            </div>
                                            <div class="form-floating w-25 ">
                                                <input type="number" step="1" name="mark" class="form-control"
                                                    placeholder="" value="5" required>
                                                <label>Marks</label>
                                            </div>
                                        </div>
                                        <div class="h4">
                                            Only mark the correct answer:
                                        </div>
                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio" value="1"
                                                    name="correct_option_${question_count}" required>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option A"
                                                name="option_1" required>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio" value="2"
                                                    name="correct_option_${question_count}" required>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option B"
                                                name="option_2" required>
                                        </div>
                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio" value="3"
                                                    name="correct_option_${question_count}" required>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option C"
                                                name="option_3" required>
                                        </div>
                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio" value="4"
                                                    name="correct_option_${question_count}" required>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option D"
                                                name="option_4" required>
                                        </div>

                                    </div>
                                </div>
            `
        );
        $('#question_count').text(question_count);
        update_marks();

    });

    $('#add_question_edit').click(function (e) {
        e.preventDefault();
        question_count_edit++;

        $('#question_container2').append(
            `
             <div class="border m-3  p-0  question-div">
                                    <div class="d-flex m-1 justify-content-end">
                                        <button type="button" id="delete_question2" class="btn btn-close">
                                    </div>
                                    <div class="p-3 pt-0">


                                        <div class="input-group mb-3">
                                            <div class="form-floating  w-75">
                                                <input type="text" name="text" class="form-control" placeholder="" required>
                                                <label>Question</label>
                                            </div>
                                            <div class="form-floating w-25 ">
                                                <input type="number" step="1" name="mark" class="form-control"
                                                    placeholder="" value="5" required>
                                                <label>Marks</label>
                                            </div>
                                        </div>
                                        <div class="h4">
                                            Only mark the correct answer:
                                        </div>
                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio" value="1"
                                                    name="correct_option_${question_count_edit}" required>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option A"
                                                name="option_1" required>
                                        </div>

                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio" value="2"
                                                    name="correct_option_${question_count_edit}" required>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option B"
                                                name="option_2" required>
                                        </div>
                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio" value="3"
                                                    name="correct_option_${question_count_edit}" required>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option C"
                                                name="option_3" required>
                                        </div>
                                        <div class="input-group mb-3">
                                            <div class="input-group-text">
                                                <input class="form-check-input mt-0 correct-option" type="radio" value="4"
                                                    name="correct_option_${question_count_edit}" required>
                                            </div>
                                            <input type="text" class="form-control" placeholder="Option D"
                                                name="option_4" required>
                                        </div>

                                    </div>
                                </div>
            `
        );
        $('#question_count_edit').text(question_count_edit);
        // update_marks();

    });
    $(document).on('input', "[name='mark']", function () {
        if ($(this).val() < 0 || isNaN($(this).val()) || $(this).val() == '') {
            $(this).val(0);
        }
        $(this).val(parseInt($(this).val()));
        update_marks();
    });

    $('#edit_quiz').submit(function (e) {
        e.preventDefault();
        data = new FormData(this);
        data.append('id', quiz_id);
        $.ajax({
            type: "PUT",
            url: "/api/quizzes",
            data: data,
            dataType: false,
            contentType: false,  // Set to false for FormData
            processData: false,

            success: function (data) {

                const myModal2 = bootstrap.Modal.getInstance($('#edit_quiz_modal'));
                myModal2.hide();

                update_quizzes_list(course_id);
            }
        }).always(function () {
            get_flash();
        });
    });
});