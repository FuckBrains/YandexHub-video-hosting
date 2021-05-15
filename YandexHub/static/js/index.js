// delete video
async function delete_video(video_id) {
    let response = await fetch('/api/video/delete/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            video_id: video_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        await location.replace('/');
    };
};

// delete article
async function delete_article(article_id) {
    let response = await fetch('/api/article/delete/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            article_id: article_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        await location.replace(`/channel/${result.data.user_id}/community/`);
    };
};

// like article
async function like_article(article_id) {
    let response = await fetch('/api/article/like/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            article_id: article_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.like == 1 && result.data.dislike == 0) {
            let like = document.getElementById(`like_article_${article_id}`)
            like.className = "btn btn-reaction-active"
            like.innerHTML = `${result.data.stats.likes} 👍`
            
            let dislike = document.getElementById(`dislike_article_${article_id}`)
            dislike.className = "btn btn-reaction"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else if (result.data.like == 0 && result.data.dislike == 0) {
            let like = document.getElementById(`like_article_${article_id}`)
            like.className = "btn btn-reaction"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById(`dislike_article_${article_id}`)
            dislike.className = "btn btn-reaction"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else {
            console.log('👻');
        };

        // alert
        await view_alert(result.message);

    };
};

// dislike article 
async function dislike_article(article_id) {
    let response = await fetch('/api/article/dislike/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            article_id: article_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.like == 0 && result.data.dislike == 1) {
            let dislike = document.getElementById(`dislike_article_${article_id}`)
            dislike.className = "btn btn-reaction-active"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`

            let like = document.getElementById(`like_article_${article_id}`)
            like.className = "btn btn-reaction"
            like.innerHTML = `${result.data.stats.likes} 👍`
        } else if (result.data.like == 0 && result.data.dislike == 0) {
            let like = document.getElementById(`like_article_${article_id}`)
            like.className = "btn btn-reaction"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById(`dislike_article_${article_id}`)
            dislike.className = "btn btn-reaction"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else {
            console.log('👻');
        };

        // alert
        await view_alert(result.message);

    };
};

// notifications
async function notifications(user_id) {
    let response = await fetch('/api/channel/notifications/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            user_id: user_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.notification == 1) {
            let notifications = document.getElementById('notifications')
            notifications.className = "btn btn-notifications-active"
        } else {
            let notifications = document.getElementById('notifications')
            notifications.className = "btn btn-notifications"
        };

        // alert
        await view_alert(result.message);
    };
};

// save video
async function save_video(video_id) {
    let response = await fetch('/api/video/save/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            video_id: video_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.save == 1) {
            let like = document.getElementById('save')
            like.className = "btn btn-save-active"
        } else {
            let like = document.getElementById('save')
            like.className = "btn btn-save"
        };

        // alert
        await view_alert(result.message);
    };
};

// like video
async function like_video(video_id) {
    let response = await fetch('/api/video/like/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            video_id: video_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.like == 1 && result.data.dislike == 0) {
            let like = document.getElementById('like')
            like.className = "btn btn-reaction-active btn-like"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById('dislike')
            dislike.className = "btn btn-reaction btn-dislike"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else if (result.data.like == 0 && result.data.dislike == 0) {
            let like = document.getElementById('like')
            like.className = "btn btn-reaction btn-like"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById('dislike')
            dislike.className = "btn btn-reaction btn-dislike"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else {
            console.log('👻');
        };

        // alert
        await view_alert(result.message);


        // ratio
        let ratio = document.getElementById('ratio-dislikes');
        if (result.data.stats.likes == 0 && result.data.stats.dislikes == 0) {
            ratio.style.width = '140px';
            ratio.style.background = '#7D7D7D';
        } else {
            ratio.style.background = '#DC3545';
            ratio.style.width = `${1.4 * (result.data.stats.dislikes * 100 / (result.data.stats.likes + result.data.stats.dislikes))}px`;
        }
    };
};

// dislike video 
async function dislike_video(video_id) {
    let response = await fetch('/api/video/dislike/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            video_id: video_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.like == 0 && result.data.dislike == 1) {
            let dislike = document.getElementById('dislike')
            dislike.className = "btn btn-reaction-active btn-dislike"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`

            let like = document.getElementById('like')
            like.className = "btn btn-reaction btn-like"
            like.innerHTML = `${result.data.stats.likes} 👍`
        } else if (result.data.like == 0 && result.data.dislike == 0) {
            let like = document.getElementById('like')
            like.className = "btn btn-reaction btn-like"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById('dislike')
            dislike.className = "btn btn-reaction btn-dislike"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else {
            console.log('👻');
        };

        // alert
        await view_alert(result.message);

        // ratio
        let ratio = document.getElementById('ratio-dislikes');
        if (result.data.stats.likes == 0 && result.data.stats.dislikes == 0) {
            ratio.style.width = '140px';
            ratio.style.background = '#7D7D7D';
        } else {
            ratio.style.background = '#DC3545';
            ratio.style.width = `${1.4 * (result.data.stats.dislikes * 100 / (result.data.stats.likes + result.data.stats.dislikes))}px`;
        }
    };
};

// subscribe to user
async function subscribe(channel_id) {
    let response = await fetch('/api/channel/subscribe/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            channel_id: channel_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.subscribe == 1) {
            let subscribe = document.getElementById('subscribe')
            subscribe.className = "btn btn-warning btn-subscribe"
            subscribe.innerHTML = "Subscribed"

        } else {
            let subscribe = document.getElementById('subscribe')
            subscribe.className = "btn btn-danger btn-subscribe"
            subscribe.innerHTML = "Subscribe"
        };

        // alert
        await view_alert(result.message);
    };
};


// add comment
async function add_comment(video_id, text) {
    let response = await fetch('/api/comment/add/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            video_id: video_id,
            text: text
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        await view_alert(result.message);
    } else {
        await view_alert(result.message);
    };
};

// like comment
async function like_comment(comment_id) {
    let response = await fetch('/api/comment/like/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            comment_id: comment_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.like == 1 && result.data.dislike == 0) {
            let like = document.getElementById(`like_comment_${comment_id}`)
            like.className = "btn btn-reaction-active"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById(`dislike_comment_${comment_id}`)
            dislike.className = "btn btn-reaction"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else if (result.data.like == 0 && result.data.dislike == 0) {
            let like = document.getElementById(`like_comment_${comment_id}`)
            like.className = "btn btn-reaction"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById(`dislike_comment_${comment_id}`)
            dislike.className = "btn btn-reaction"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else {
            console.log('👻');
        };

        // alert
        //await view_alert(result.message);

    };
};

// dislike comment 
async function dislike_comment(comment_id) {
    let response = await fetch('/api/comment/dislike/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            comment_id: comment_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.like == 0 && result.data.dislike == 1) {
            let dislike = document.getElementById(`dislike_comment_${comment_id}`)
            dislike.className = "btn btn-reaction-active"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`

            let like = document.getElementById(`like_comment_${comment_id}`)
            like.className = "btn btn-reaction"
            like.innerHTML = `${result.data.stats.likes} 👍`
        } else if (result.data.like == 0 && result.data.dislike == 0) {
            let like = document.getElementById(`like_comment_${comment_id}`)
            like.className = "btn btn-reaction"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById(`dislike_comment_${comment_id}`)
            dislike.className = "btn btn-reaction"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else {
            console.log('👻');
        };

        // alert
        //await view_alert(result.message);

    };
};

// delete comment 
async function delete_comment(comment_id) {
    let response = await fetch('/api/comment/delete/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            comment_id: comment_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        let comment = document.getElementById(`comment_${comment_id}`)
        comment.remove()
    } else {
        console.log('👻');
    };

    // alert
    await view_alert(result.message);
};


// add reply comment
async function add_reply_comment(video_id, comment_id, text) {
    let response = await fetch('/api/comment/reply/add/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            video_id: video_id,
            comment_id: comment_id,
            text: text
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        await view_alert(result.message);
    } else {
        await view_alert(result.message);
    };
};

// like reply comment
async function like_reply_comment(reply_comment_id) {
    let response = await fetch('/api/comment/reply/like/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            reply_comment_id: reply_comment_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.like == 1 && result.data.dislike == 0) {
            let like = document.getElementById(`like_reply_comment_${reply_comment_id}`)
            like.className = "btn btn-reaction-active"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById(`dislike_reply_comment_${reply_comment_id}`)
            dislike.className = "btn btn-reaction"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else if (result.data.like == 0 && result.data.dislike == 0) {
            let like = document.getElementById(`like_reply_comment_${reply_comment_id}`)
            like.className = "btn btn-reaction"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById(`dislike_reply_comment_${reply_comment_id}`)
            dislike.className = "btn btn-reaction"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else {
            console.log('👻');
        };

        // alert
        //await view_alert(result.message);

    };
};

// dislike reply comment 
async function dislike_reply_comment(reply_comment_id) {
    let response = await fetch('/api/comment/reply/dislike/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            reply_comment_id: reply_comment_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.like == 0 && result.data.dislike == 1) {
            let dislike = document.getElementById(`dislike_reply_comment_${reply_comment_id}`)
            dislike.className = "btn btn-reaction-active"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`

            let like = document.getElementById(`like_reply_comment_${reply_comment_id}`)
            like.className = "btn btn-reaction"
            like.innerHTML = `${result.data.stats.likes} 👍`
        } else if (result.data.like == 0 && result.data.dislike == 0) {
            let like = document.getElementById(`like_reply_comment_${reply_comment_id}`)
            like.className = "btn btn-reaction"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById(`dislike_reply_comment_${reply_comment_id}`)
            dislike.className = "btn btn-reaction"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else {
            console.log('👻');
        };

        // alert
        //await view_alert(result.message);

    };
};

// delete reply comment 
async function delete_reply_comment(reply_comment_id) {
    let response = await fetch('/api/comment/reply/delete/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            reply_comment_id: reply_comment_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        let comment = document.getElementById(`reply_comment_${reply_comment_id}`)
        comment.remove()
    } else {
        console.log('👻');
    };

    // alert
    await view_alert(result.message);
};


// buy a film
async function buy_film(film_id) {
    let response = await fetch('/api/buy/film/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            film_id: film_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        await location.replace(`/film/${film_id}/`);
    };
};

// like film
async function like_film(film_id) {
    let response = await fetch('/api/film/like/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            film_id: film_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.like == 1 && result.data.dislike == 0) {
            let like = document.getElementById('like_film')
            like.className = "btn btn-reaction-active btn-like"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById('dislike_film')
            dislike.className = "btn btn-reaction btn-dislike"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else if (result.data.like == 0 && result.data.dislike == 0) {
            let like = document.getElementById('like_film')
            like.className = "btn btn-reaction btn-like"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById('dislike_film')
            dislike.className = "btn btn-reaction btn-dislike"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else {
            console.log('👻');
        };

        // alert
        await view_alert(result.message);

        // ratio
        let ratio = document.getElementById('ratio-dislikes-film');
        if (result.data.stats.likes == 0 && result.data.stats.dislikes == 0) {
            ratio.style.width = '140px';
            ratio.style.background = '#7D7D7D';
        } else {
            ratio.style.background = '#DC3545';
            ratio.style.width = `${1.4 * (result.data.stats.dislikes * 100 / (result.data.stats.likes + result.data.stats.dislikes))}px`;
        }
    };
};

// dislike film 
async function dislike_film(film_id) {
    let response = await fetch('/api/film/dislike/', {
        method: 'POST',
        headers: { 'X-CSRFToken': getCookie('csrftoken'), 'Content-Type': 'application/json' },
        body: JSON.stringify({
            film_id: film_id
        })
    });
    let result = await response.json();
    if (result.status == "ok") {
        if (result.data.like == 0 && result.data.dislike == 1) {
            let dislike = document.getElementById('dislike_film')
            dislike.className = "btn btn-reaction-active btn-dislike"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`

            let like = document.getElementById('like_film')
            like.className = "btn btn-reaction btn-like"
            like.innerHTML = `${result.data.stats.likes} 👍`
        } else if (result.data.like == 0 && result.data.dislike == 0) {
            let like = document.getElementById('like_film')
            like.className = "btn btn-reaction btn-like"
            like.innerHTML = `${result.data.stats.likes} 👍`

            let dislike = document.getElementById('dislike_film')
            dislike.className = "btn btn-reaction btn-dislike"
            dislike.innerHTML = `${result.data.stats.dislikes} 👎`
        } else {
            console.log('👻');
        };

        // alert
        await view_alert(result.message);

        // ratio
        let ratio = document.getElementById('ratio-dislikes-film');
        if (result.data.stats.likes == 0 && result.data.stats.dislikes == 0) {
            ratio.style.width = '140px';
            ratio.style.background = '#7D7D7D';
        } else {
            ratio.style.background = '#DC3545';
            ratio.style.width = `${1.4 * (result.data.stats.dislikes * 100 / (result.data.stats.likes + result.data.stats.dislikes))}px`;
        }
    };
};

