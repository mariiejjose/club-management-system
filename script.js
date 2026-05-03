const API = "https://such-hemlock-pug.ngrok-free.dev";

let selectedEventId = null;

/* ================= HELPERS ================= */

async function safeFetch(url, options = {}) {
    try {
        const res = await fetch(url, options);

        if (!res.ok) {
            throw new Error(`HTTP error ${res.status}`);
        }

        return await res.json();
    } catch (err) {
        console.error("Fetch error:", err);
        alert("Server connection failed. Make sure backend + ngrok are running.");
        throw err;
    }
}

/* ================= LOGIN ================= */

async function login() {
    const email = document.getElementById("email").value;
    const password = document.getElementById("password").value;

    const data = await safeFetch(`${API}/login`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ email, password })
    });

    alert(data.message);

    if (data.user_id) {
        localStorage.setItem("user_id", data.user_id);
        window.location.href = "index.html";
    }
}

/* ================= REGISTER ================= */

async function register() {
    const name = document.getElementById("name").value.trim();
    const email = document.getElementById("email").value.trim();
    const password = document.getElementById("password").value.trim();
    const confirmPassword = document.getElementById("confirmPassword").value.trim();

    if (!name || !email || !password || !confirmPassword) {
        return alert("Fill all fields");
    }

    if (password !== confirmPassword) {
        return alert("Passwords do not match");
    }

    const data = await safeFetch(`${API}/register`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ name, email, password })
    });

    alert(data.message);
}

/* ================= CLUBS ================= */

async function loadClubs() {
    const clubList = document.getElementById("clubList");
    if (!clubList) return;

    const clubs = await safeFetch(`${API}/clubs`);

    clubList.innerHTML = "";

    clubs.forEach(club => {
        const div = document.createElement("div");

        div.innerHTML = `
            <strong>${club.name}</strong><br>
            ${club.description}<br><br>
            <button onclick="joinClub(${club.id})">Join</button>
            <button onclick="leaveClub(${club.id})">Leave</button>
            <hr>
        `;

        clubList.appendChild(div);
    });
}

async function joinClub(id) {
    const user_id = localStorage.getItem("user_id");

    const data = await safeFetch(`${API}/join_club`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_id, club_id: id })
    });

    alert(data.message);
}

async function leaveClub(id) {
    const user_id = localStorage.getItem("user_id");

    const data = await safeFetch(`${API}/leave_club`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_id, club_id: id })
    });

    alert(data.message);
}

/* ================= EVENTS ================= */

async function loadEvents() {
    const eventList = document.getElementById("eventList");
    if (!eventList) return;

    const events = await safeFetch(`${API}/events`);

    eventList.innerHTML = "";

    events.forEach(event => {
        const div = document.createElement("div");

        div.innerHTML = `
            <strong>${event.name}</strong><br>
            ${event.description}<br><br>
            <button onclick="joinEvent(${event.id})">Register</button>
            <button onclick="leaveEvent(${event.id})">Cancel</button>
            <hr>
        `;

        eventList.appendChild(div);
    });
}

async function joinEvent(id) {
    const user_id = localStorage.getItem("user_id");

    const data = await safeFetch(`${API}/join_event`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_id, event_id: id })
    });

    alert(data.message);
}

async function leaveEvent(id) {
    const user_id = localStorage.getItem("user_id");

    const data = await safeFetch(`${API}/leave_event`, {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ user_id, event_id: id })
    });

    alert(data.message);
}

/* ================= MEMBERS ================= */

async function loadMembers() {
    const list = document.getElementById("memberList");
    if (!list) return;

    const users = await safeFetch(`${API}/members`);

    list.innerHTML = "";

    users.forEach(user => {
        const div = document.createElement("div");

        div.innerHTML = `
            <strong>${user.username}</strong><br>
            Clubs: ${user.clubs.length ? user.clubs.join(", ") : "None"}
            <hr>
        `;

        list.appendChild(div);
    });
}

/* ================= USERS ================= */

async function loadUsers() {
    const list = document.getElementById("userList");
    if (!list) return;

    const users = await safeFetch(`${API}/users`);

    list.innerHTML = "";

    users.forEach(user => {
        const div = document.createElement("div");

        div.innerHTML = `
            <strong>${user.username}</strong><br>
            <button onclick="deleteUser(${user.id})">Delete</button>
            <hr>
        `;

        list.appendChild(div);
    });
}

async function deleteUser(id) {
    if (!confirm("Delete user?")) return;

    const data = await safeFetch(`${API}/delete_user/${id}`, {
        method: "DELETE"
    });

    alert(data.message);
    loadUsers();
}

/* ================= AUTO LOAD ================= */

window.onload = function () {
    loadClubs();
    loadEvents();
    loadMembers();
    loadUsers();
};