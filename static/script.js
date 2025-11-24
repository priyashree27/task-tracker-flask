// Load tasks when page opens
window.onload = fetchTasks;

// ---------------- Fetch All Tasks ----------------
function fetchTasks() {
    fetch("/api/tasks")
        .then(res => res.json())
        .then(tasks => {
            let list = document.getElementById("taskList");
            list.innerHTML = "";

            tasks.forEach(task => {
                list.innerHTML += `
                    <li>
                        <span style="text-decoration:${task.status === 'completed' ? 'line-through' : 'none'}">
                            ${task.title}
                        </span>

                        <div>
                            <button onclick="toggleStatus(${task.id}, '${task.status}')">✔</button>
                            <button onclick="deleteTask(${task.id})">🗑</button>
                        </div>
                    </li>
                `;
            });
        });
}

// ---------------- Add New Task ----------------
function addTask() {
    let task = document.getElementById("taskInput").value.trim();
    if (task === "") return;

    fetch("/api/tasks", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ title: task })
    })
    .then(() => {
        document.getElementById("taskInput").value = "";
        fetchTasks();
    });
}

// ---------------- Toggle Status (Pending ↔ Completed) ----------------
function toggleStatus(id, currentStatus) {
    let newStatus = currentStatus === "pending" ? "completed" : "pending";

    fetch(`/api/tasks/${id}`, {
        method: "PUT",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({ status: newStatus })
    })
    .then(fetchTasks);
}

// ---------------- Delete Task ----------------
function deleteTask(id) {
    fetch(`/api/tasks/${id}`, { method: "DELETE" })
        .then(fetchTasks);
}
