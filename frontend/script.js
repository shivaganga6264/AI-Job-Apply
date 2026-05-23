const applyBtn =
    document.getElementById("applyBtn");

const statusText =
    document.getElementById("status");

const countText =
    document.getElementById("count");

const historyDiv =
    document.getElementById("history");


// Load Application History
async function loadHistory() {

    try {

        const response = await fetch(
            "http://127.0.0.1:8000/history"
        );

        const history = await response.json();

        historyDiv.innerHTML = "";

        history.reverse().forEach(job => {

            historyDiv.innerHTML += `

                <div class="job-card">

                    <h4>${job.title}</h4>

                    <p>${job.company}</p>

                    <p>${job.time}</p>

                </div>
            `;
        });

    }

    catch (error) {

        console.log(error);
    }
}


// Apply Jobs
applyBtn.addEventListener(
    "click",

    async () => {

        statusText.innerText =
            "Applying Jobs...";

        try {

            const response = await fetch(

                "http://172.20.10.2:8000/apply-jobs",

                {
                    method: "POST"
                }
            );

            const data =
                await response.json();

            countText.innerText =
                data.total_applied;

            statusText.innerText =
                "Application Completed ✅";

            // Reload History
            loadHistory();

        }

        catch (error) {

            statusText.innerText =
                "Error Applying Jobs ❌";

            console.log(error);
        }
    }
);


// Load History On Page Open
loadHistory();
if ("serviceWorker" in navigator) {

    navigator.serviceWorker.register(
        "service-worker.js"
    )

    .then(() => {

        console.log(
            "Service Worker Registered"
        );
    });
}