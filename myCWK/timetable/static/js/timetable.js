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

        eventMouseEnter: function(info) {
            let tooltip = document.createElement("div");
            tooltip.classList.add("event-tooltip");
            tooltip.innerHTML = `
                <strong>${info.event.title}</strong><br>
                <small>Teacher: ${info.event.extendedProps.teacher || "Unknown"}</small><br>
                <small>Location: ${info.event.extendedProps.location || "Unknown"}</small>
            `;
            tooltip.style.position = "absolute";
            tooltip.style.backgroundColor = "#000";
            tooltip.style.color = "#fff";
            tooltip.style.padding = "5px";
            tooltip.style.borderRadius = "5px";
            tooltip.style.top = `${info.jsEvent.clientY + 10}px`;
            tooltip.style.left = `${info.jsEvent.clientX + 10}px`;
            tooltip.style.zIndex = "1000";
            tooltip.setAttribute("id", "event-tooltip");
            document.body.appendChild(tooltip);
        },

        eventMouseLeave: function() {
            let tooltip = document.getElementById("event-tooltip");
            if (tooltip) tooltip.remove();
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

            console.log("✅ Event Clicked:", event.title, "ID:", event.id);

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
