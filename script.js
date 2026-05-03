// ------------------ AUTH ------------------

async function register() {
    const username = document.querySelector("input[type='email']").value;
    const password = document.querySelectorAll("input[type='password']")[0].value;

    const response = await fetch("http://127.0.0.1:5000/register", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();
    alert(data.message);
}

async function login() {
    const username = document.querySelector("input[type='email']").value;
    const password = document.querySelector("input[type='password']").value;

    const response = await fetch("http://127.0.0.1:5000/login", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ username, password })
    });

    const data = await response.json();

    if (response.status === 200) {
        localStorage.setItem("user_id", data.user_id);
        alert("Login successful");
        window.location.href = "index.html";
    } else {
        alert(data.message);
    }
}

// ------------------ ADMIN ACCESS ------------------

function openAdmin() {
    const password = prompt("Enter admin password:");
    if (password === "admin123") {
        window.location.href = "admin.html";
    } else {
        alert("Wrong password");
    }
}

// ------------------ CLUBS ------------------

async function createClub() {
    const name = document.getElementById("clubName").value;
    const description = document.getElementById("clubDesc").value;

    const response = await fetch("http://127.0.0.1:5000/create_club", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, description })
    });

    const data = await response.json();
    alert(data.message);
}

async function loadClubs() {
    const response = await fetch("http://127.0.0.1:5000/clubs");
    const clubs = await response.json();

    const list = document.getElementById("clubList");
    list.innerHTML = "";

    clubs.forEach(club => {
        list.innerHTML += `
            <strong>${club.name}</strong><br>
            ${club.description}<br>
            <button onclick="joinClub(${club.id})">Join</button>
            <button onclick="leaveClub(${club.id})">Leave</button>
            <hr>
        `;
    });
}

async function joinClub(id) {
    const user_id = localStorage.getItem("user_id");

    await fetch("http://127.0.0.1:5000/join_club", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_id, club_id: id })
    });

    alert("Joined club");
}

async function leaveClub(id) {
    const user_id = localStorage.getItem("user_id");

    await fetch("http://127.0.0.1:5000/leave_club", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_id, club_id: id })
    });

    alert("Left club");
}

// ------------------ EVENTS ------------------

async function createEventAdmin() {
    const name = document.getElementById("eventName").value;
    const description = document.getElementById("eventDesc").value;

    const response = await fetch("http://127.0.0.1:5000/create_event", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, description })
    });

    const data = await response.json();
    alert(data.message);
}

async function loadEvents() {
    const response = await fetch("http://127.0.0.1:5000/events");
    const events = await response.json();

    const list = document.getElementById("eventList");
    list.innerHTML = "";

    events.forEach(event => {
        list.innerHTML += `
            <strong>${event.name}</strong><br>
            ${event.description}<br>
            <button onclick="joinEvent(${event.id})">Register</button>
            <button onclick="leaveEvent(${event.id})">Cancel</button>
            <hr>
        `;
    });
}

async function joinEvent(id) {
    const user_id = localStorage.getItem("user_id");

    await fetch("http://127.0.0.1:5000/join_event", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_id, event_id: id })
    });

    alert("Registered for event");
}

async function leaveEvent(id) {
    const user_id = localStorage.getItem("user_id");

    await fetch("http://127.0.0.1:5000/leave_event", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_id, event_id: id })
    });

    alert("Registration cancelled");
}

// ------------------ ADMIN EVENT/CLUB MANAGEMENT ------------------

let selectedEventId = null;

async function loadEventsForEdit() {
    const response = await fetch("http://127.0.0.1:5000/events");
    const events = await response.json();

    const list = document.getElementById("eventList");
    list.innerHTML = "";

    events.forEach(event => {
        list.innerHTML += `
            <strong>${event.name}</strong><br>
            ${event.description}<br>
            <button onclick="selectEvent(${event.id}, '${event.name}', '${event.description}')">Edit</button>
            <hr>
        `;
    });
}

function selectEvent(id, name, description) {
    selectedEventId = id;
    document.getElementById("editName").value = name;
    document.getElementById("editDesc").value = description;
}

async function updateEvent() {
    const name = document.getElementById("editName").value;
    const description = document.getElementById("editDesc").value;

    const response = await fetch(`http://127.0.0.1:5000/update_event/${selectedEventId}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, description })
    });

    const data = await response.json();
    alert(data.message);
    loadEventsForEdit();
}

// delete event
async function loadEventsForDelete() {
    const response = await fetch("http://127.0.0.1:5000/events");
    const events = await response.json();

    const list = document.getElementById("eventList");
    list.innerHTML = "";

    events.forEach(event => {
        list.innerHTML += `
            <strong>${event.name}</strong><br>
            ${event.description}<br>
            <button onclick="deleteEventAdmin(${event.id})">Delete</button>
            <hr>
        `;
    });
}

async function deleteEventAdmin(id) {
    await fetch(`http://127.0.0.1:5000/delete_event/${id}`, { method: "DELETE" });
    alert("Event deleted");
    loadEventsForDelete();
}

// delete club
async function loadClubsForDelete() {
    const response = await fetch("http://127.0.0.1:5000/clubs");
    const clubs = await response.json();

    const list = document.getElementById("clubList");
    list.innerHTML = "";

    clubs.forEach(club => {
        list.innerHTML += `
            <strong>${club.name}</strong><br>
            ${club.description}<br>
            <button onclick="deleteClub(${club.id})">Delete</button>
            <hr>
        `;
    });
}

async function deleteClub(id) {
    await fetch(`http://127.0.0.1:5000/delete_club/${id}`, { method: "DELETE" });
    alert("Club deleted");
    loadClubsForDelete();
}

// members
async function loadMembers() {
    const response = await fetch("http://127.0.0.1:5000/members");
    const users = await response.json();

    const list = document.getElementById("memberList");
    list.innerHTML = "";

    users.forEach(user => {
        list.innerHTML += `
            <strong>${user.username}</strong><br>
            Clubs: ${user.clubs.join(", ") || "None"}
            <hr>
        `;
    });
}

// manage users
async function loadUsers() {
    const response = await fetch("http://127.0.0.1:5000/users");
    const users = await response.json();

    const list = document.getElementById("userList");
    list.innerHTML = "";

    users.forEach(user => {
        list.innerHTML += `
            <strong>${user.username}</strong><br>
            <button onclick="deleteUser(${user.id})">Delete</button>
            <hr>
        `;
    });
}

async function deleteUser(id) {
    await fetch(`http://127.0.0.1:5000/delete_user/${id}`, { method: "DELETE" });
    alert("User deleted");
    loadUsers();
}