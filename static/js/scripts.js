$(function() {
    $("#period-start").datepicker({
        format:'yyyy-mm-dd',
    });
    $("#period-end").datepicker({
        format:'yyyy-mm-dd',
    });

    $('#calendar-dates').on('click', '.Calendar__col', function(e) {
        e.preventDefault();
        var long_date = $(this).next('input').val();

        $.get(`http://localhost:8000/visits/${long_date}`, (data) => {
            console.log('calling');
            var offset_height = $('#calendar').outerHeight();
            $('#dog-data').animate({
                top: `${50 + offset_height}px`,
                opacity: 1,
            }, 1000, () => {})

            var html = '';

            for (const [_, dog_data] of Object.entries(data.dogs)){
                console.log(dog_data);
                html += `
                    <div class="row d-flex flex-row">
                        <div class="col-3 text-center">
                            Dog ${dog_data.n + 1}
                        </div>
                        <div class="col-3 text-center">
                            ${dog_data.fullname}
                        </div>
                        <div class="col-3 text-center">
                            ${dog_data.startdate}
                        </div>
                        <div class="col-3 text-center">
                            ${dog_data.enddate}
                        </div>
                    </div>
                `;
            }

            $('#dog-data').html(html);
        })
    })

    $('#period-confirm').click((event) => {
        var period_start = $("#period-start").val();
        var period_end = $("#period-end").val();

        if (!period_start || !period_end) return;

        if (period_start > period_end) {
            alert('Period start should be before period end, or at least the same.');
            return;
        }

        $.get(`http://localhost:8000/visits/?period_start=${period_start}&period_end=${period_end}`, (data) => {
            // $('#calendar').css('display', 'block');
            $('#calendar').animate({
                top: '0px',
                opacity: 1,
            }, 1000, () => {});

            var html = '';

            for (const [key, value] of Object.entries(data.calendar)){
                console.log(key, value);

                if($.isEmptyObject(value)){
                    html += '<div class="Calendar__col"></div>';
                    continue;
                }

                html += `
                    <div class="Calendar__col">
                        <div class="Calendar__col--info d-flex flex-column justify-content-center">
                            <small>${value.short_date}</small>
                            <p>${value.dog_count} dogs</p>
                        </div>
                    </div>
                    <input value="${value.long_date}" type="hidden"/>
                `;
            }
            $('#calendar-dates').html(html);
        });
    })
})