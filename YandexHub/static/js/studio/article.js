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
        for (i in result.data.views) {
            days.push(i);
            likes.push(result.data.likes[i]);
            dislikes.push(result.data.dislikes[i]);
        };
        await likes_and_dislikes_stats(days.reverse(), likes.reverse(), dislikes.reverse());
    };
};

async function likes_and_dislikes_stats(days, likes, dislikes) {
    'use strict'

    feather.replace()

    // Graphs
    var ctx = document.getElementById('likes_and_dislkes')
    // eslint-disable-next-line no-unused-vars

    var Disikes = new Chart(ctx, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                data: dislikes,
                lineTension: 0,
                backgroundColor: 'transparent',
                borderColor: '#000',
                borderWidth: 4,
                pointBackgroundColor: '#000'
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

    var Likes = new Chart(ctx, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                data: likes,
                lineTension: 0,
                backgroundColor: 'transparent',
                borderColor: '#E81224',
                borderWidth: 4,
                pointBackgroundColor: '#E81224'
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
