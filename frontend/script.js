const API = "http://127.0.0.1:5000";

// login
async function login() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;

    const response = await fetch(`${API}/login`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    const data = await response.json();

    alert(data.message);

    if (response.status === 200) {
        localStorage.setItem("user_id", data.user_id);
        window.location.href = "index.html";
    }
}

// register
async function register() {
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    const confirmPassword = document.getElementById("confirmPassword").value;

    if (password !== confirmPassword) {
        alert("Passwords do not match");
        return;
    }

    const response = await fetch(`${API}/register`, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            username: username,
            password: password
        })
    });

    const data = await response.json();

    alert(data.message);

    if (response.status === 200) {
        window.location.href = "login.html";
    }
}

// clubs
async function loadClubs() {
    const response = await fetch("http://127.0.0.1:5000/clubs");
    const clubs = await response.json();

    const clubList = document.getElementById("clubList");
    clubList.innerHTML = "";

    clubs.forEach(club => {
        const div = document.createElement("div");
        div.className = "btn";

        div.innerHTML = `
            <strong>${club.name}</strong><br>
            ${club.description}<br><br>
            <button onclick="joinClub(${club.id})">Join</button>
            <button onclick="leaveClub(${club.id})">Leave</button>
        `;

        clubList.appendChild(div);
    });
}

async function joinClub(clubId) {
    const userId = localStorage.getItem("user_id");

    const response = await fetch("http://127.0.0.1:5000/join_club", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: userId,
            club_id: clubId
        })
    });

    const data = await response.json();
    alert(data.message);
}

async function leaveClub(clubId) {
    const userId = localStorage.getItem("user_id");

    const response = await fetch("http://127.0.0.1:5000/leave_club", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: userId,
            club_id: clubId
        })
    });

    const data = await response.json();
    alert(data.message);
}

//events
async function loadEvents() {
    const response = await fetch("http://127.0.0.1:5000/events");
    const events = await response.json();

    const eventList = document.getElementById("eventList");
    eventList.innerHTML = "";

    events.forEach(event => {
        const div = document.createElement("div");
        div.className = "btn";

        div.innerHTML = `
            <strong>${event.name}</strong><br>
            ${event.description}<br><br>
            <button onclick="joinEvent(${event.id})">Register</button>
            <button onclick="leaveEvent(${event.id})">Cancel</button>
        `;

        eventList.appendChild(div);
    });
}

async function joinEvent(eventId) {
    const userId = localStorage.getItem("user_id");

    console.log("User:", userId, "Event:", eventId);

    const response = await fetch("http://127.0.0.1:5000/join_event", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: userId,
            event_id: eventId
        })
    });

    const data = await response.json();
    alert(data.message);
}

async function leaveEvent(eventId) {
    const userId = localStorage.getItem("user_id");

    console.log("User:", userId, "Event:", eventId);

    const response = await fetch("http://127.0.0.1:5000/leave_event", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: userId,
            event_id: eventId
        })
    });

    const data = await response.json();
    alert(data.message);
}

async function createClub() {
    const name = document.getElementById("clubName").value;
    const description = document.getElementById("clubDesc").value;

    if (!name || !description) {
        alert("Please fill all fields");
        return;
    }

    const response = await fetch("http://127.0.0.1:5000/create_club", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            name: name,
            description: description
        })
    });

    const data = await response.json();
    alert(data.message);
}

function openAdmin() {
    const password = prompt("Enter admin password:");

    if (password === "admin123") {
        window.location.href = "admin.html";
    } else {
        alert("Wrong password");
    }
}

async function loadClubsForDelete() {
    const response = await fetch("http://127.0.0.1:5000/clubs");
    const clubs = await response.json();

    const list = document.getElementById("clubList");
    list.innerHTML = "";

    clubs.forEach(club => {
        const div = document.createElement("div");

        div.innerHTML = `
            <strong>${club.name}</strong><br>
            ${club.description}<br><br>
            <button onclick="deleteClub(${club.id})">Delete</button>
            <hr>
        `;

        list.appendChild(div);
    });
}

async function deleteClub(id) {
    const confirmDelete = confirm("Are you sure you want to delete this club?");

    if (!confirmDelete) return;

    const response = await fetch(`http://127.0.0.1:5000/delete_club/${id}`, {
        method: "DELETE"
    });

    const data = await response.json();
    alert(data.message);

    loadClubsForDelete(); // refresh list
}

async function deleteClub(id) {
    const confirmDelete = confirm("Are you sure you want to delete this club?");

    if (!confirmDelete) return;

    const response = await fetch(`http://127.0.0.1:5000/delete_club/${id}`, {
        method: "DELETE"
    });

    const data = await response.json();
    alert(data.message);

    loadClubsForDelete(); // refresh list
}
