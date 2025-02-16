function openConfirmationModal(event) {
    let eventId = event.id || event.extendedProps.id; 
    console.log("Opening Confirmation Modal for Event ID:", eventId);

    fetch(`/modal/confirm/${eventId}/`)
    .then(response => response.text())
    .then(html => {
        let modalDiv = document.createElement('div');
        modalDiv.innerHTML = html;
        document.body.appendChild(modalDiv);

        let modal = new bootstrap.Modal(modalDiv.querySelector(".modal"));
        modal.show();
    });
}

function openEditModal(event) {
    let eventId = event.id || event.extendedProps.id;
    console.log("Opening Edit Modal for Event ID:", eventId);

    fetch(`/modal/edit/${eventId}/`)
    .then(response => response.text())
    .then(html => {
        let modalDiv = document.createElement('div');
        modalDiv.innerHTML = html;
        document.body.appendChild(modalDiv);

        let modal = new bootstrap.Modal(modalDiv.querySelector(".modal"));
        modal.show();
    });
}

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
            console.log("✅ Event Mounted:", info.event.title, info.event.id);
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
            console.log("✅ Event Clicked:", info.event);
            console.log("🔹 Event ID:", info.event.id || info.event.extendedProps.id);
            console.log("🔹 Event Type:", info.event.extendedProps.type);

            if (!info.event.extendedProps.type) {
                console.error("❌ Event Type is MISSING. Check event creation logic.");
                return;
            }

            if (info.event.extendedProps.type === "admin") {
                openConfirmationModal(info.event);
            } else {
                openEditModal(info.event);
            }
        }
    });

    calendar.render();
});


// Open the modal for adding a new session
document.getElementById("add-session-btn").addEventListener("click", function() {
    var modal = new bootstrap.Modal(document.getElementById("session-modal"));
    modal.show();
});

// AJAX - Submitting a new session without reloading the page
document.getElementById("add-session-form").addEventListener("submit", function(event) {
    event.preventDefault();
    let formData = new FormData(this);

    let csrfToken = document.querySelector("[name=csrfmiddlewaretoken]").value;

    fetch("/timetable/add-session/", {
        method: "POST",
        body: formData,
        headers: { "X-CSRFToken": csrfToken }
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            alert("Session Added!");
            var modal = bootstrap.Modal.getInstance(document.getElementById("session-modal"));
            modal.hide();
            location.reload();
        } else {
            alert("Error adding session!");
        }
    });
});
