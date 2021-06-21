async function get_video_stats(video_id) {
    let response = await fetch('/api/video/stats/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            video_id: video_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        views = []
        comments = []
        likes = []
        dislikes = []
        days = []
        for (i in result.data.views) {
            days.push(i);
            views.push(result.data.views[i]);
            comments.push(result.data.comments[i])
            likes.push(result.data.likes[i]);
            dislikes.push(result.data.dislikes[i]);
        };

        await views_stats(days.reverse(), views.reverse());
        await likes_stats(days.reverse(), likes.reverse());
        await dislikes_stats(days.reverse(), dislikes.reverse());
        await comments_stats(days.reverse(), comments.reverse());
    };
};

async function views_stats(days, views) {
    'use strict'

    feather.replace()

    // Graphs
    var ctx = document.getElementById('views')
    // eslint-disable-next-line no-unused-vars
    var Views = new Chart(ctx, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                data: views,
                lineTension: 0,
                backgroundColor: 'transparent',
                borderColor: '#007bff',
                borderWidth: 4,
                pointBackgroundColor: '#007bff'
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
    })
};

async function comments_stats(days, comments) {
    'use strict'

    feather.replace()

    // Graphs
    var ctx = document.getElementById('comments')
    // eslint-disable-next-line no-unused-vars
    var Comments = new Chart(ctx, {
        type: 'line',
        data: {
            labels: days,
            datasets: [{
                data: comments,
                lineTension: 0,
                backgroundColor: 'transparent',
                borderColor: '#007bff',
                borderWidth: 4,
                pointBackgroundColor: '#007bff'
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
    })
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