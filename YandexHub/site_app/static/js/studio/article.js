async function get_article_stats(article_id) {
    let response = await fetch('/api/article/stats/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            article_id: article_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        likes = []
        dislikes = []
        days = []
        for (i in result.data.likes) {
            days.push(i);
            likes.push(result.data.likes[i]);
            dislikes.push(result.data.dislikes[i]);
        };
 
        await likes_stats(days.reverse(), likes.reverse());
        await dislikes_stats(days.reverse(), dislikes.reverse());
    };
};

async function likes_stats(days, likes) {
    'use strict'

    feather.replace()

    // Graphs
    var ctx = document.getElementById('likes')
    
    // eslint-disable-next-line no-unused-vars
    var Likes = new Chart(ctx, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                data: likes,
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


async function dislikes_stats(days, dislikes) {
    'use strict'

    feather.replace()

    // Graphs
    var ctx = document.getElementById('dislkes')

    // eslint-disable-next-line no-unused-vars
    var Disikes = new Chart(ctx, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                data: dislikes,
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
