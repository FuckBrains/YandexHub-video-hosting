async function get_track_stats(track_id) {
    let response = await fetch('/api/track/stats/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            track_id: track_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        auditions = []
        days = []
        for (i in result.data.auditions) {
            days.push(i);
            auditions.push(result.data.auditions[i]);
        };
 
        await auditions_stats(days.reverse(), auditions.reverse());
    };
};

async function auditions_stats(days, auditions) {
    'use strict'

    feather.replace()

    // Graphs
    var ctx = document.getElementById('auditions')
    
    // eslint-disable-next-line no-unused-vars
    var Auditions = new Chart(ctx, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                data: auditions,
                lineTension: 0,
                backgroundColor: 'transparent',
                borderColor: '#0D6EFD',
                borderWidth: 4,
                pointBackgroundColor: '#0D6EFD'
            }]
        },
        options: {
            scales: {
                yAxes: [{
                    ticks: {
                        beginAtZero: true
                    }
                }]
            },
            legend: {
                display: false
            }
        }
    });
};


