document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');

    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridWeek',
        height: "auto",
        headerToolbar: {
            left: 'prev,next today',
            center: 'title',
            right: 'dayGridMonth,timeGridWeek,timeGridDay'
        },
        views: {
            dayGridMonth: { buttonText: 'Month' },
            timeGridWeek: { buttonText: 'Week' },
            timeGridDay: { buttonText: 'Day' }
        },
        events: '/timetable/get-events/',

        eventDidMount: function(info) {
            if (info.event.extendedProps.type === "admin") {
                info.el.style.backgroundColor = "red";  // Admin event color
            } else {
                info.el.style.backgroundColor = "blue"; // Student event color
            }
        },


        editable: true,

        eventDrop: function(info) {
            if (info.event.extendedProps.type === "admin") {
                alert("You cannot modify an assigned event.");
                info.revert();
            }
        },

        eventClick: function(info) {
            let event = info.event;


            // Prevent editing of admin-assigned events
            if (event.extendedProps.type === "admin") {
                alert("❌ You cannot edit an admin-assigned event.");
                return;
            }

            // Redirect user to the edit page for this event
            window.location.href = `/timetable/edit-event/${event.id}/`;
        }


    });

    calendar.render();
});


document.getElementById("add-session-btn").addEventListener("click", function() {
    window.location.href = "/timetable/add-session/";
});
