function fetchSummary() {
    fetch('/api/summary')
        .then(response => response.json())
        .then(data => {
            const presentStudents = data.present_students;
            const absentStudents = data.absent_students;

            const presentTable = document.getElementById('present-table-body');
            const absentTable = document.getElementById('absent-table-body');

            presentTable.innerHTML = '';
            absentTable.innerHTML = '';

            presentStudents.forEach(student => {
                const row = document.createElement('tr');
                const nameCell = document.createElement('td');
                const timeCell = document.createElement('td');

                nameCell.textContent = student.name;
                timeCell.textContent = student.time;

                row.appendChild(nameCell);
                row.appendChild(timeCell);
                presentTable.appendChild(row);
            });

            absentStudents.forEach(student => {
                const row = document.createElement('tr');
                const nameCell = document.createElement('td');
                nameCell.textContent = student;
                row.appendChild(nameCell);
                absentTable.appendChild(row);
            });
        })
        .catch(error => {
            console.error('Error fetching summary:', error);
        });
}


setInterval(fetchSummary, 5000);
window.onload = fetchSummary;