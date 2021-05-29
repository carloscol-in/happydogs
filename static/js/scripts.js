$(function() {
    $("#period-start").datepicker({
        format:'yyyy-mm-dd',
    });
    $("#period-end").datepicker({
        format:'yyyy-mm-dd',
    });

    $('#period-confirm').click((event) => {
        var period_start = $("#period-start").val();
        var period_end = $("#period-end").val();

        if (!period_start || !period_end) return;

        if (period_start > period_end) {
            alert('Period start should be before period end, or at least the same.');
            return;
        }

        $.get(`http://localhost:8000/visits/?period_start=${period_start}&period_end=${period_end}`, (data) => {
            // console.log(data);
            var html = '';
            for (const [key, value] of Object.entries(data.calendar)){
                console.log(key, value);

                if($.isEmptyObject(value)){
                    html += '<div class="Calendar__col"></div>';
                    continue;
                }

                html += `
                    <div class="Calendar__col">
                        <small>${value.long_date}</small>
                        <small>${value.short_date}</small>
                        <p>${value.dog_count}</p>
                    </div>
                `;
            }
            $('#calendar-dates').html(html);
        });
    })
})